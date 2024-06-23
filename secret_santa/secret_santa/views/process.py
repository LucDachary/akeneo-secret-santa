from django.views.generic.edit import FormView

from secret_santa.forms import ProcessForm


class ProcessView(FormView):
    """A form to submit a list of Secret Santa participants and start the processing.
    """
    template_name = "process.html"
    form_class = ProcessForm
    success_url = "/"

    def form_valid(self, form):
        # OK
        # TODO write a message to the end user
        return super().form_valid(form)
