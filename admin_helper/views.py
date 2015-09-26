# encoding: utf-8
import json

from django.db.models import Q
from django.template import RequestContext
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, Http404

from admin_helper.settings import SU_KEY


class AdminHelperMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user or not request.user.is_superuser and SU_KEY not in request.session:
            raise Http404()

        return super(AdminHelperMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminHelperMixin, self).get_context_data(**kwargs)
        context['original_username'] = self.request.session.get(SU_KEY) or u''
        context['in_su'] = context['original_username'] and context['original_username'] != self.request.user.username
        context['path'] = self.request.META.get('HTTP_REFERER') or self.request.path
        return context


class SuggestView(AdminHelperMixin, ListView):
    """
    * Фильтровать по разрешенным параметрам
    * Рендерить сразу в шаблон

    $.ajax({
        url: '/suggest/',
        dataType: 'json',
        method: 'get',
        data: {
            meta_name: $(input).val(),
            is_active: null,
            template: 'users/suggest_user.html'
        }
    })
        .success(function(response){
            $('.user_list').html(response.html);    
        })
    """
    model = get_user_model()
    template_name = 'admin_helper/card_list.html'
    allowed_params = ['limit', 'is_active', 'meta_name', 'order_by']

    def get_queryset(self):
        qs = super(SuggestView, self).get_queryset()

        term = self.request.GET.get('meta_name')
        if term:
            qs = qs.filter(
                Q(first_name__icontains=term) |
                Q(last_name__icontains=term) |
                Q(username__icontains=term) |
                Q(email__icontains=term)
            )

        order_by = self.request.GET.get('order_by')
        if order_by:
            qs = qs.order_by(order_by)

        limit = self.request.GET.get('limit')
        if limit:
            qs = qs[:limit]

        return qs

    def get_template_names(self):
        result = super(SuggestView, self).get_template_names()
        result = self.request.GET.get('t', result)
        return result

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax() or self.request.GET.get('format') == 'json':
            response = super(SuggestView, self).render_to_response(context, **response_kwargs)

            if response.template_name:
                data = {
                    'result': u'OK',
                    'data': response.rendered_content,
                }
            else:
                data = []
                for user in response.context_data.get('object_list'):
                    data.append(user.as_json() if hasattr(user, 'as_json') else {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    })

                data = {
                    'result': u'OK',
                    'data': data,
                }

            response = JsonResponse(data)
        else:
            raise Http404()

        return response


class PopupView(AdminHelperMixin, TemplateView):
    template_name = 'admin_helper/popup.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax() or self.request.GET.get('format') == 'json':
            response = super(PopupView, self).render_to_response(context, **response_kwargs)
            response = JsonResponse({
                'result': u'OK',
                'data': response.rendered_content,
            })
        else:
            raise Http404()

        return response
