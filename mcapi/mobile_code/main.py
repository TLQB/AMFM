import kivy
from kivy.utils import platform
from kivy.app import App
from kivy.uix.label import Label

if platform == "android":
    from jnius import autoclass

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

kv = """
BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'Create Topic'
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: topic
        Button:
            text: 'Create'
            on_press: app.create_topic()
"""


class MyApp(App):
    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions(
            [
                Permission.ACCESS_COARSE_LOCATION,
                Permission.ACCESS_FINE_LOCATION,
            ],
            callback,
        )

    def build(self):
        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return Builder.load_string(kv)

    # def on_start(self):
    #     from kivy import platform
    #     if platform == "android":
    #         self.start_service()

    def create_topic(self):
        topic = "rgps/" + self.root.ids.topic.text
        print(topic)

        from kivy import platform

        if platform == "android":
            self.start_service(topic)

        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()

    @staticmethod
    def start_service(topic):
        from jnius import autoclass

        service = autoclass("org.test.gpsdemo.ServiceTrackinggps")
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        service.start(mActivity, topic)
        return service


if __name__ == "__main__":
    MyApp().run()