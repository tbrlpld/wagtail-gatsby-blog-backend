# -*- coding: utf-8 -*-

"""
Custom GraphQL schema types that are not supported natively by Grapple.

Importing the grapple types does not work, because they depend on the
apps being registered.

```python
from grapple.types.images import ImageObjectType  # noqa: E800
# -> django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
```

graphene.Union fails. It can not work with the string identified types
the way that graphene.List does.
Therefore, I can not return all tagged items in one type. The different
returned elements need to have their own tag type each.

"""
import typing as ty

from django.db import models as djm  # type: ignore

from wagtail.documents.models import get_document_model   # type: ignore
from wagtail.images import get_image_model   # type: ignore

from taggit import models as tgm   # type: ignore

import graphql  # type: ignore
import graphene  # type: ignore
import graphene_django  # type: ignore


class TagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        description="Type for a general taggit.Tag"


class ImageTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        exclude = ('blog_blogpagetag_items',)
        description="Tag used on images."

    tagged_images = graphene.List("grapple.types.images.ImageObjectType")

    def resolve_tagged_images(self, _):
        image_model = get_image_model()

        return image_model.objects.filter(tags__id=self.id)


class DocumentTagType(graphene_django.DjangoObjectType):
    class Meta:
        model = tgm.Tag
        exclude = ('blog_blogpagetag_items',)
        description="Tag used on documents."

    tagged_documents = graphene.List("grapple.types.documents.DocumentObjectType")

    def resolve_tagged_documents(self, _):
        document_model = get_document_model()

        return document_model.objects.filter(tags__id=self.id)


class Query(graphene.ObjectType):  # noqa: WPS214
    """Queries regarding the tagging system."""

    tag = graphene.Field(
        TagType,
        id_=graphene.ID(name='id'),
        name=graphene.String(),
    )
    tags = graphene.List(TagType)

    def resolve_tag(
        self,
        _,
        id_: ty.Optional[int] = None,
        name: ty.Optional[str] = None,
    ) -> tgm.Tag:
        """
        Return tag identified by its id or name.

        Parameters
        ----------
        _
            unused
        id_: int
            Id of the tag to return.
        name: str
            `name` property of the  tag to return.

        Returns
        -------
        tgm.Tag
            Tag with the given `id` or `name` and used to tag at least one
            image.

        Raises
        ------
        GraphQLError
            Raised if neither `tag_id` or `tag_name` are defined, which is
            needed to return the given tag.

        """
        if id_ is not None:
            return tgm.Tag.objects.get(pk=id_)
        if name is not None:
            return tgm.Tag.objects.get(name=name)
        raise graphql.GraphQLError(
            'Id or name of the tag needs to be defined to return it.',
        )

    def resolve_tags(self, _) -> djm.QuerySet:  # noqa: D102
        """
        Return all tags.

        Parameters
        ----------
        _
            unused. Only present because the info dict is automatically
            injected by Graphene.

        Returns
        -------
        django.db.model.QuerySet
            Django query set of tags (`taggit.models.Tag`).

        """
        return tgm.Tag.objects.all().order_by('pk')

    @staticmethod  # noqa: WPS602
    def get_model_specific_tags(model_name: str) -> djm.QuerySet:
        """
        Get all tags used on a given content type model.

        Parameters
        ----------
        model_name : str
            E.g. passing the string `image` will return all tags that have been
            used to tag items with the content type `image`.

        Returns
        -------
        djm.QuerySet
            Dajgno queryset of tags (`taggit.model.Tags`) used to tag the
            given model's content type.

        """
        return tgm.Tag.objects.filter(
            taggit_taggeditem_items__content_type__model=model_name,
        )

    @staticmethod
    def get_tags_of_model_instance(
        model: djm.Model,
        primary_key: ty.Optional[int] = None,
        title: ty.Optional[str] = None,
    ) -> djm.QuerySet:
        """
        Return all tags of a given models instance.

        The model is passed and the instance is identified by either its
        `id` or `title` property.

        Parameters
        ----------
        model : djm.Model
            Django model for which to return the tags.
        primary_key : ty.Optional[int]
            Primary key to identify the instance for which to return the tags.
        title : ty.Optional[str]
            Title of the instance for which to return the tags. This is
            mainly meant for the Wagtail image and document model.

        Returns
        -------
        djm.QuerySet
            Django query set of tags (`taggit.models.Tag`) used to tag the
            identified model instance.

        Raises
        ------
        GraphQLError
            Raised if neither `primary_key` or `title` are defined, which is
            needed to identify the model instance and return its tags.

        """
        if primary_key is not None:
            return model.objects.get(pk=primary_key).tags.all()
        if title is not None:
            return model.objects.get(title=title).tags.all()
        raise graphql.GraphQLError(
            'Id or title of the {model}'.format(model=model.__name__.lower())
            + ' needs to be defined to return its tags.',
        )

    image_tag = graphene.Field(
        ImageTagType,
        tag_id=graphene.ID(),
        tag_name=graphene.String(),
    )
    image_tags = graphene.List(ImageTagType)
    tags_of_image = graphene.List(
        ImageTagType,
        image_id=graphene.ID(),
        image_title=graphene.String(),
    )

    def resolve_image_tag(
        self,
        _,
        tag_id: ty.Optional[int] = None,
        tag_name: ty.Optional[str] = None,
    ) -> tgm.Tag:
        """
        Return a specific image tag.

        Image tags are once that have been used to tag at least one image.

        Parameters
        ----------
        _
            unused
        tag_id: int
            Id of the image tag to return
        tag_name: str
            `name` property of the image tag to return

        Returns
        -------
        tgt.Tag or None
            Tag with the given `id` or `name` and used to tag at least one
            image.

        Raises
        ------
        GraphQLError
            Raised if neither `tag_id` or `tag_name` are defined, which is
            needed to return the given tag.

        """
        image_tags = Query.get_model_specific_tags('image')
        if tag_id is not None:
            return image_tags.get(pk=tag_id)
        if tag_name is not None:
            return image_tags.get(name=tag_name)
        raise graphql.GraphQLError(
            'Id or name of the image tag needs to be defined to return it.',
        )

    def resolve_image_tags(self, _) -> djm.QuerySet:
        """
        Return all tags used to tag at least one image.

        Parameters
        ----------
        _
            unused

        Returns
        -------
        djm.QuerySet
            Django queryset of all tags used on at least one image.

        """
        return Query.get_model_specific_tags('image').order_by('pk')

    def resolve_tags_of_image(
        self,
        _,
        image_id: ty.Optional[int] = None,
        image_title: ty.Optional[str] = None,
    ) -> djm.QuerySet:
        """
        Return all tags of an image.

        Parameters
        ----------
        _
            unused
        image_id: ty.Optional[int]
            Id of the image for which to return all tags.
        image_title: ty.Optional[str]
            Title of the image for which to return all tags.

        Returns
        -------
        djm.QuerySet
            Django queryset of all tags (`taggit.models.Tag`) used on the
            identified image.

        """
        return Query.get_tags_of_model_instance(
            get_image_model(),
            primary_key=image_id,
            title=image_title,
        )

    document_tag = graphene.Field(
        DocumentTagType,
        id_=graphene.ID(name='id'),
        name=graphene.String(),
    )
    document_tags = graphene.List(DocumentTagType)
    tags_of_document = graphene.List(
        DocumentTagType,
        document_id=graphene.ID(),
        document_title=graphene.String(),
    )

    def resolve_document_tag(
        self,
        _,
        tag_id: ty.Optional[int] = None,
        tag_name: ty.Optional[str] = None,
    ) -> tgm.Tag:
        """
        Return a specific document tag.

        Document tags are once that have been used to tag at least one
        document.

        Parameters
        ----------
        _
            unused
        tag_id: int
            Id of the document tag to return
        tag_name: str
            `name` property of the tag to return

        Returns
        -------
        tgm.Tag
            Tag with the given `id` or `name` and used to tag at least one
            document.

        Raises
        ------
        GraphQLError
            Raised if neither `tag_id` or `tag_name` are defined, which is
            needed to return the given tag.

        """
        document_tags = Query.get_model_specific_tags('document')
        if tag_id is not None:
            return document_tags.get(pk=tag_id)
        if tag_name is not None:
            return document_tags.get(name=tag_name)
        raise graphql.GraphQLError(
            'Id or name of the document tag needs to be defined to return it.',
        )

    def resolve_document_tags(self, _):
        """
        Return all tags used to tag at least one document.

        Parameters
        ----------
        _
            unused

        Returns
        -------
        djm.QuerySet
            Django queryset of all tags used on at least one document.

        """
        return Query.get_model_specific_tags('document').order_by('pk')

    def resolve_tags_of_document(
        self,
        _,
        document_id: ty.Optional[int] = None,
        document_title: ty.Optional[str] = None,
    ):
        """
        Return all tags of an document.

        Parameters
        ----------
        _
            unused
        document_id: ty.Optional[int]
            Id of the document for which to return all tags.
        document_title: ty.Optional[str]
            Title of the document for which to return all tags.

        Returns
        -------
        djm.QuerySet
            Django queryset of all tags (`taggit.models.Tag`) used on the
            identified document.

        """
        return Query.get_tags_of_model_instance(
            get_document_model(),
            primary_key=document_id,
            title=document_title,
        )
