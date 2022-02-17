Version 0.1.26 (17.02.2022)
***************************
- Only show return Categories with at least one active Slideshow
- Rework SlideshowEndpoint, only retunr SlideshowPage ids in LIST, and full object in detail
- Provide Title Image for Categories
- Make it possible to have GlossaryEntries that have either a text or just Links
- Sort GlosarryEntries by Alphabet

Version 0.1.25 (08.11.2021)
***************************
- Minor fixes to SlideShows

Version 0.1.24 (04.10.2021)
***************************
- Add "Categories" to SlideshowAdmin

Version 0.1.23 (20.09.2021)
***************************
- Add django-taggit to requirements
- Add Categroies to slideshow model

Version 0.1.22 (02.09.2021)
***************************
- Amend field ordering in MediaObject inlines.

Version 0.1.21 (01.09.2021)
***************************
Version 0.1.21a3 (19.07.2021)
***************************
- Fix sample project
- Fix Condition in MediaFileField to recognize all variations of jpg and jpeg fiel extensions
- Return dict of kind `{ "original": <url>}`  for audio and video files

Version 0.1.21a3 (03.07.2021)
***************************
- Add proxy model migrations
- Add missing attribute to Meta class of proxy models


Version 0.1.21a2 (08.06.2021)
***************************
- Fix naming issues
- add MediaObject Endpoint to project urls.py
- fix import error

Version 0.1.21a1 (07.06.2021)
***************************
- Add media_object app as extension of photpgraph app.
- Fix the static filtering in the message app.
- Make the subject of the emails sent by the contact app dynamically add the PROJECT_NAME

Version 0.1.19 (05.05.2021)
***************************
- Hotfix contact App.


Version 0.1.16 (24.02.2021)
***************************
- Rename the Slideshow and SlideshowImage 'img' fields
- Add tests for relationship fields
- Create admin action that switches Deep Zoom image options
- Fix false declared 'required' attribute of some fields in swagger
- Fix swagger crash caused by a self-referential TreeNodeSerializer field


Version 0.1.15 (16.02.2021)
***************************
- TreeNode fields are modified
- BaseProfile has an additional TreeForeignKey field to TreeNode
- TreeNodeSerializer is adapted and improved
- FieldMappingsEndpoint is removed
- Tests for BaseProfile and TreeNode are added
- ProfileEndpoint provides Photographs ordered by profile_position


Version 0.1.14 (27.01.2021)
***************************
- SlideshowEndpoint provides only active objects ordered by position
- GlossaryEntryEndpoint provides objects ordered by term


Version 0.1.13 (23.01.2021)
***************************
- Add ConcatCharField and FromToConcatField fields


Version 0.1.12 (16.11.2020)
***************************
- Add active and position field to Slideshow model.
- Implement position validation for Slideshow, SlideshowPage, SlideshowImage models.
- Add profile position field to Photograph model.
- Implement PhotographInlineFormSet for profile position validation.


Version 0.1.11 (23.09.2020)
***************************
- Replace image fields with relations to the Photograph model in Message, QuizQuestion,
  Slideshow, SlideshowImage models and adjust the serializers accordingly.
- Delete no more needed HasImgForm.


Version 0.1.9 (27.08.2020)
***************************
- Make porfiles explicitly not required in TreeNode serializer.


Version 0.1.8 (27.08.2020)
***************************
- Deep Zoom image option is available for Photograph model.
- Add media configuration to settings of the sample project.
- Set time zone to "Europe/Berlin" in the sample project.


Version 0.1.6 (28.07.2020)
***************************
- Display automatically populated fields in the Photograph admin interface.
- Amend error messages in HasImgForm and DateOrderForm.


Version 0.1.5 (22.07.2020)
***************************
- Change `valid_to` field to optional in Message model. (`valid_to`=NULL stands for endless.)
- Adjust validation of `valid_from` and `valid_to`.
- Adjust `messages` Endpoint accordingly.
- Add Photograph `form`, `extra` and `fields` ordering to PhotographInline.


Version 0.1.4  (07.07.2020)
***************************
- Oopsie forgot to take notes.


Version 0.1.1  (29.06.2020)
***************************
- Add overall description and License.


Version 0.1.0  (29.06.2020)
***************************
- First release of the package
