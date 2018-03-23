from django.core.management.base import BaseCommand


class DBReadonlyCommand(BaseCommand):
    # Since we are not creating database content with the command this should
    # be a safe thing to do.
    # The reason for disabling locale is to be able to use mock_open. If it is
    # enabled then tests will start failing due to open() being mocked and not
    # returning a proper file object which is needed in some version of django
    # when it runs a command.
    #
    # https://docs.djangoproject.com/en/2.0/howto/custom-management-commands
    # /django.core.management.BaseCommand.leave_locale_alone
    leave_locale_alone = True
