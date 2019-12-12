from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import (
    ObjectProperty, StringProperty, DictProperty, BooleanProperty, NumericProperty)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView
from methods import *
import math
import os


class Container(BoxLayout):

    def start(self):
        try:
            self.output_key.text = ''
            self.output_text.text = ''
            self.input_text.text = ''
            filename = self.input_file_name.text
            with open(filename, 'rb') as f:
                input_text = f.read()
            if self.type_of_code.text == 'Шифрование':
                self.make_encode(input_text)
            else:
                self.make_decode(input_text)
        except FileNotFoundError:
            self.lbl_error_file.color = (1, 0, 0, 1)

    def make_encode(self, input_text):
        filename = self.input_file_name.text
        try:
            if self.key_p.text == self.key_q.text:
                raise ValueError_p
            if not self.key_p.text.isdigit() or not self.check_prime(int(self.key_p.text)):
                raise ValueError_p
            if not self.key_q.text.isdigit() or not self.check_prime(int(self.key_q.text)):
                raise ValueError_q
            if not self.close_key.text.isdigit():
                raise ValueError_close
            if int(self.key_p.text) * int(self.key_q.text) < 256:
                raise ValueError_r
            euler_fun = (int(self.key_p.text) - 1) * (int(self.key_q.text) - 1)
            if self.key_is_not_right(int(self.close_key.text), euler_fun):
                raise ValueError_close
            open_key = rsa_encode(self.input_file_name.text,
                       int(self.key_p.text), int(self.key_q.text), int(self.close_key.text))
            filetemp = filename + '.cph'
            file_out = open(filetemp, 'rb')
            self.output_key.text = str(open_key)
            a = min(len(input_text), 32)
            b = min(os.path.getsize(filetemp), 32)
            size = b // a
            print(size)
            for i in range(a):
                self.input_text.text += str(input_text[i]) + ' '
            for i in range(a):
                result = 0
                for j in range(size): 
                    chunk = file_out.read(1) 
                    result = result*256 + chunk[0]
                self.output_text.text += str(result) + ' '
            file_out.close()
            self.r_number = int(self.key_p.text) * int(self.key_q.text)

        except ValueError_p:
            self.lbl_error_key_p.color = (1, 0, 0, 1)
        except ValueError_q:
            self.lbl_error_key_q.color = (1, 0, 0, 1)
        except ValueError_close:
            self.lbl_error_close_key.color = (1, 0, 0, 1)
        except ValueError_r:
            self.lbl_error_key_r.color = (1, 0, 0, 1)

    def make_decode(self, input_text):
        filename = self.input_file_name.text
        try:
            if not self.key_q.text.isdigit():
                raise ValueError_q
            if not self.close_key.text.isdigit():
                raise ValueError_close
            if (int(self.close_key.text) >= int(self.key_q.text)) or (
                 int(self.key_q.text) < 256):
                raise ValueError_close
            result = rsa_decode(self.input_file_name.text,
                       int(self.key_q.text), int(self.close_key.text))
            if result:
                raise ValueError_close
            else:
                if filename[len(filename) - 4:] == '.cph':
                    filetemp = filename[:(len(filename) - 4)]
                    temp = filetemp.partition('.')
                    filetemp = temp[0] + '(copy)' + temp[1] + temp[2]
                    file_out = open(filetemp, 'rb')
                else:
                    filetemp = filename + '.cph'
                    file_out = open(filetemp, 'rb')
                a = min(len(input_text), 32)
                b = min(os.path.getsize(filetemp), 32)
                print(a, b)
                size = a // b
                for i in range(b):
                    result = 0
                    for j in range(size):
                        result = result * 256 + input_text[i*size+j]
                    self.input_text.text += str(result) + ' '
                for i in range(b):
                    chunk = file_out.read(1)
                    self.output_text.text += str(chunk[0]) + ' '
            file_out.close()
        except ValueError_q:
            self.lbl_error_key_q.color = (1, 0, 0, 1)
        except ValueError_close:
            self.lbl_error_close_key.color = (1, 0, 0, 1)

    @staticmethod
    def check_prime(number):
        root = int(math.sqrt(number))
        if number < 2:
            return False
        for divider in range(2, root):
            if number % divider == 0:
                return False
        return True

    @staticmethod
    def key_is_not_right(key, euler_fun):
        if not (1 < key < euler_fun):
            return True
        NOD = Euklid_algoritm(euler_fun, key)
        if NOD != 1:
            return True
        return False


class InputKey(TextInput):
    pass


class BtnOpenFile(Button):

    def get_path(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests/')


class MethodSpinner(Spinner):

    active_method = StringProperty('Шифрование')

    def clean_input(self):
        root = App.get_running_app().root.get_screen('main').container
        if self.active_method != self.text:
            self.active_method = self.text
            if self.text == 'Шифрование':
                root.key_p.opacity = 1
                root.lbl_p.opacity = 1
                root.lbl_q.text = 'Число q'
                root.key_q.text = ''
            else:
                root.key_p.opacity = 0
                root.lbl_p.opacity = 0
                root.lbl_q.text = 'Число r'
                if root.r_number:
                    root.key_q.text = str(root.r_number)
            root.key_p.text = ''
            root.output_key.text = ''
            root.output_text.text = ''
            root.input_file_name.text = ''
            root.input_text.text = ''


class MainScreen(Screen):
    pass


class FileChooserScreen(Screen):
    pass


class ChoosingFile(FileChooserIconView):

    def fill_text(self):
        self._update_files()
        root = App.get_running_app().root
        root.current = 'main'
        if self.selection != []:
            root.get_screen('main').container.input_file_name.text = (
                self.selection[0].replace('tests/', '', 1))


class MyApp(App):

    def build(self):
        sm = ScreenManager()
        self.sm = sm
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(FileChooserScreen(name='filechooser'))
        return self.sm


class ValueError_p(Exception):
    pass


class ValueError_q(Exception):
    pass


class ValueError_close(Exception):
    pass


class ValueError_r(Exception):
    pass


if __name__ == '__main__':
    MyApp().run()
