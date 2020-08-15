# -*- coding: utf-8 -*-

"""Extend the `DocumentObjectType` provided by  `wagtail-grapple`."""

from django.conf import settings
import wagtail
import graphene
import grapple


def get_document_url(cls):
    url = ''
    if hasattr(cls, 'url'):
        url = cls.url
    else:
        url = cls.file.url

    if url[0] == '/':
        return settings.BASE_URL + url
    return url


class ExtendedDocumentObjectType(grapple.types.documents.DocumentObjectType):
    class Meta:
        model = wagtail.documents.get_document_model()
        exclude_fields = ("tags",)

    src = graphene.String()

    def resolve_src(self, info):
        """Get URL of the document."""
        return get_document_url(self)


class Query(graphene.ObjectType):
    documents_extended = graphene.List(
        ExtendedDocumentObjectType,
        id_=graphene.ID(name='id'),
    )

    def resolve_documents_extended(self, info, id_=None):
        doc_model = wagtail.documents.get_document_model()
        if not id_:
            return doc_model.objects.all().order_by('pk')
        return doc_model.objects.all().filter(pk=id_)
