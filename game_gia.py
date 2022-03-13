from kivy.app import App, Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

import abc
import threading
import number_exam
import common_letters


class Menu(BoxLayout, Screen):
    """
    Assigns the proper screen for a given test
    set the needed extra layout
    and generates the first question.
    """
    def go_to_a_screen_test(self, screen_name: str):
        """"""
        app.root.current = screen_name
        screen = app.root.current_screen
        ratio_boxtest = screen.ids.boxtest.size_hint
        boxtest_real_size = [a*b for a,b in zip(screen.ids.boxtest.size_hint,Window.size)]
        # boxtest_x = ratio_boxtest[0] * Window.size[0]
        # boxtest_y = ratio_boxtest[1] * Window.size[1]
        screen.design(boxtest_real_size)
        screen.update_layout_with_new_question()
        screen.start_timer()


class SingleTestInterface(BoxLayout, Screen):
    """Interface for all the different test screens classes"""
    def __init__(self, **kwargs):
        __metaclass__ = abc.ABCMeta
        super(SingleTestInterface, self).__init__(**kwargs)
        self.question: str = ''
        self.answer: str = ''
        self.score: int = 0
        self.number_of_questions: int = 1
        self.widgets: dict = {'buttons': {}, 'labels':{}, 'grid':{}}
        self.timer: threading.Timer = None

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'design') and
                callable(subclass.design) and
                hasattr(subclass, 'update_layout_with_new_question') and
                callable(subclass.update_layout_with_new_question) or
                NotImplemented)

    @abc.abstractmethod
    def design(self,size):
        """Designs specific layout for a given test"""
        pass

    @abc.abstractmethod
    def update_layout_with_new_question(self):
        """Generates a new question and assigns it to the layout of a given test"""
        pass

    def check_answer_update_score_and_add_new_question(self, button: Button):
        """Compares the user's answer with the expected answer"""
        if button.text == str(self.answer):
            self.score += 1
        else:
            self.score -= 1
        self.update_layout_with_new_question()
        self.number_of_questions += 1


    def stop_game(self):
        """ When the timer is done, disable all buttons and show the user score"""
        for value in self.widgets['buttons'].values():
            value.disabled = True
        self.ids.score_lbl.text = f'Your score is {self.score}\n' \
                                  f'There was {self.number_of_questions} questions'

    def start_timer(self):
        """Timer to start when a test is starting"""
        self.timer = threading.Timer(3, self.stop_game)
        self.timer.start()

    def remove_test_layout(self):
        """
        Reset the screen and variables to their original layout/values
        Set the 'menu' screen as the current one
        """
        self.timer.cancel()
        # Loop through the range of the length of children because
        # when looping through the children, some were missed and
        # I couldn't figure out why

        for n in range(len(self.ids.boxtest.children)):
            self.ids.boxtest.remove_widget(self.ids.boxtest.children[0])
        self.ids.score_lbl.text = ''
        self.score = 0
        self.number_of_questions = 1
        app.root.current = 'menu'


class NumbersTest(SingleTestInterface):

    def design(self,boxtest_real_size):
        h_layout_x = boxtest_real_size[0]/3*2
        h_layout_y = boxtest_real_size[1]/3*2
        h_layout_pos_x = boxtest_real_size[0]/6
        h_layout_pos_y = boxtest_real_size[1]/6

        h_layout = BoxLayout(size=(h_layout_x,h_layout_y),
                             pos=(h_layout_pos_x,h_layout_pos_y),
                             size_hint=(None,None))
        for n in range(3):
            b_name = f'button_{n+1}'
            button = Button(text='', on_release=self.check_answer_update_score_and_add_new_question,
                            font_size=30, disabled=False)
            self.widgets['buttons'][b_name] = button
            h_layout.add_widget(button)
        self.ids.boxtest.add_widget(h_layout)

    def update_layout_with_new_question(self):
        self.question, self.answer = number_exam.get_question_and_answer()
        # Assign the 3 numbers from the question to the text of the 3 buttons
        for i, value in enumerate(self.widgets['buttons'].values()):
            value.text = str(self.question[i])

class LettersTest(SingleTestInterface):

    def design(self,boxtest_real_size):
        h_layout_x = boxtest_real_size[0]/3*2
        h_layout_y = boxtest_real_size[1]/8*7
        h_layout_pos_x = boxtest_real_size[0]/6
        h_layout_pos_y = boxtest_real_size[1]/8
        h_layout = BoxLayout(orientation='vertical',
                             size=(h_layout_x,h_layout_y),
                             pos=(h_layout_pos_x,h_layout_pos_y),
                             size_hint=(None,None))
        grid = GridLayout(cols=4, spacing=20)
        for n in range(8):
            lbl = Label(text='',font_size=60, padding_y = 20)
            grid.add_widget(lbl)
            self.widgets['grid'][f'letter_{str(n)}']=lbl
        answers_line = BoxLayout(orientation='horizontal',size = self.parent.size )
        for n in range(5):
            a_btn = Button(text=str(n),
                           on_release=self.check_answer_update_score_and_add_new_question,
                           font_size=50,
                           disabled=False)
            answers_line.add_widget(a_btn)
            self.widgets['buttons'][f'answer_{str(n)}']=a_btn
        h_layout.add_widget(grid)
        h_layout.add_widget(Label(size=(boxtest_real_size[0],boxtest_real_size[1]/9),
                                  size_hint=(None,None)))
        h_layout.add_widget(answers_line)
        self.ids.boxtest.add_widget(h_layout)

    def update_layout_with_new_question(self):
        self.question, self.answer = common_letters.get_question_and_answer()
        for label, letter in zip(self.widgets['grid'],self.question):
            self.widgets['grid'][label].text=letter
        # for letter in self.question[0]:
        #     grid.add_widget(Label(text=letter,font_size=50))
        # for letter in self.question[1]:
        #     grid.add_widget(Label(text=letter,font_size=50))
        # grid.add_widget(Label())

class LabelInputs:
    pass



class MainApp(App):

    def build(self):
        print(Window.size)
        file = Builder.load_file('gia_screens.kv')
        return file


if __name__ == '__main__':
    app = MainApp()
    app.run()
