from rick.base import Registry
from rick.mixin import Translator


class Rule:
    ERROR_ATTR = "MSG_ERROR"

    def validate(
        self, value, options: list = None, error_msg=None, translator: Translator = None
    ):
        raise NotImplementedError()

    def error_message(
        self, msg_override=None, translator: Translator = None, *args
    ) -> str:
        msg = msg_override if msg_override else getattr(self, self.ERROR_ATTR, None)
        if not msg:
            raise RuntimeError(
                "missing error message attribute '{0}' on Rule '{1}'".format(
                    self.ERROR_ATTR, str(type(self))
                )
            )

        if translator:
            msg = translator.t(msg)

        return msg.format(*args) if args else msg


# Validator registry
registry = Registry(Rule)
