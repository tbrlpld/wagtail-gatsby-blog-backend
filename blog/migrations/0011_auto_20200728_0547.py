# Generated by Django 2.2.13 on 2020-07-28 05:47

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.blocks.static_block
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200728_0540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='freeformbody',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.TextBlock()), ('email', wagtail.core.blocks.EmailBlock(help_text='Your email goes here.')), ('integer', wagtail.core.blocks.IntegerBlock(help_text='Just a number.')), ('float', wagtail.core.blocks.FloatBlock(help_text='A floating point number.')), ('decimal', wagtail.core.blocks.DecimalBlock(decimal_places=2, help_text='A decimal number.')), ('regex', wagtail.core.blocks.RegexBlock(error_messages={'invalid': 'You need to have " stuff " in the string.'}, help_text='A string with stuff in the middle.', regex='^.*stuff.*$')), ('url', wagtail.core.blocks.URLBlock()), ('bool', wagtail.core.blocks.BooleanBlock(required=False)), ('date', wagtail.core.blocks.DateBlock()), ('time', wagtail.core.blocks.TimeBlock()), ('datetime', wagtail.core.blocks.DateTimeBlock()), ('rawhtml', wagtail.core.blocks.RawHTMLBlock(help_text='Here you can show off your HTML skills.')), ('blockquote', wagtail.core.blocks.BlockQuoteBlock()), ('choice', wagtail.core.blocks.ChoiceBlock(choices=[('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')])), ('page', wagtail.core.blocks.PageChooserBlock()), ('doc', wagtail.documents.blocks.DocumentChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('static', wagtail.core.blocks.static_block.StaticBlock(admin_text='Latest Posts (no configuration needed)', help_text='If you include this block, the latest posts will be displayed here.')), ('person', wagtail.core.blocks.StructBlock([('first_name', wagtail.core.blocks.CharBlock()), ('last_name', wagtail.core.blocks.CharBlock()), ('biography', wagtail.core.blocks.TextBlock()), ('pic', wagtail.images.blocks.ImageChooserBlock(required=False))], icon='user')), ('list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(label='List Item'))), ('substream', wagtail.core.blocks.StreamBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('quote', wagtail.core.blocks.BlockQuoteBlock()), ('author', wagtail.core.blocks.CharBlock(min_length=5))]))], blank=True),
        ),
    ]
