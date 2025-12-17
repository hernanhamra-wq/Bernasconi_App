from django import forms
from .models import Investigacion

class InvestigacionForm(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = "__all__"
        widgets = {
            "detalle_investigacion": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "investigacion_id" in self.fields:
            self.fields["investigacion_id"].disabled = True
            self.fields["investigacion_id"].required = False

            # ✅ si es nuevo, mostramos "auto"
            if not self.instance or not self.instance.pk:
                self.fields["investigacion_id"].widget.attrs["placeholder"] = "auto"

            self.fields["investigacion_id"].widget.attrs["class"] = "input"
