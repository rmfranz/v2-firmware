
class PeriodicController:

    def __init__(self):
        self.auth_token_caller = None

    def set_auth_token_caller(self, caller):
        print("seteo")
        self.auth_token_caller = caller

    def start_auth_token_caller(self):
        print("starteo")
        self.auth_token_caller.start()

    def stop_auth_token_caller(self):
        print("stopeo")
        self.auth_token_caller.stop()