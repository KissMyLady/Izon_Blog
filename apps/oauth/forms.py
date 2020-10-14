# -*- coding: utf-8 -*-
from django import forms
from .models import Ouser


# 纵断面形状 简况
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Ouser
        fields = ['link', 'avatar']






