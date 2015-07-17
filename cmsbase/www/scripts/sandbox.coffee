API = require '../scripts/api.coffee'
ImageUploader = require '../scripts/image-uploader.coffee'

window.onload = () ->

    ContentTools.IMAGE_UPLOADER = ImageUploader.createImageUploader

    # Build a palette of styles
    ContentTools.StylePalette.add([
        new ContentTools.Style('By-line', 'article__by-line', ['p']),
        new ContentTools.Style('Caption', 'article__caption', ['p']),
        new ContentTools.Style('Example', 'example', ['pre']),
        new ContentTools.Style('Example + Good', 'example--good', ['pre']),
        new ContentTools.Style('Example + Bad', 'example--bad', ['pre'])
        ])

    editor = new ContentTools.EditorApp.get()
    editor.init('.editable', 'data-name')

    editor.bind 'save', (regions) ->
        console.log regions

        translationId = document.body.getAttribute('data-translation-id')

        data = 
            live_content: JSON.stringify(regions)

        API.call('post', "admin/cmsbase/page/translation/save-content/#{translationId}/", data, false)

        # Trigger a flash to indicate the save has been successful
        new ContentTools.FlashUI('ok')