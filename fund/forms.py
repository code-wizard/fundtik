import requests
from django.conf import settings
from django.db import transaction
from django.forms import ModelForm
from fund import models


class FbFundForm(ModelForm):

    class Meta:
        model = models.FbFunding
        fields = ["opening_date", "closing_date", "qualifiers", "fund_name", "agency",
                  "requirements", "key_contacts", "occurrence", "occurrence_no", "amount", "file", "categories"]

    def save(self, commit=True):
        with transaction.atomic():
            print(self.cleaned_data.get("file"), )
            file = {'file': (self.cleaned_data.get("file").name, self.cleaned_data.get("file"), "application/pdf")}

            respond = requests.post(settings.PSPDF_SERVER,
                                    files=file,
                                    headers={"Content-Type": "application/pdf",
                                             "Authorization": "Token token="+settings.PSPDF_AUTH_TOKEN})

            self.instance.document_id = respond.json().get("data").get("document_id")
            self.instance.save()
            return self.instance