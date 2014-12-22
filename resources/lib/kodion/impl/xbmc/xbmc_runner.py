__author__ = 'bromix'

import xbmc
import xbmcgui
import xbmcplugin

from ..abstract_provider_runner import AbstractProviderRunner
from ...exceptions import KodimonException
from ...items import *
from ... import constants, AbstractProvider
from . import info_labels


class XbmcRunner(AbstractProviderRunner):
    def __init__(self):
        AbstractProviderRunner.__init__(self)
        pass

    def run(self, provider, context=None):
        results = None
        try:
            results = provider.navigate(context)
        except KodimonException, ex:
            if provider.handle_exception(context, ex):
                context.log_error(ex.__str__())
                xbmcgui.Dialog().ok("Exception in ContentProvider", ex.__str__())
                pass
            return

        result = results[0]
        options = {}
        options.update(results[1])

        if isinstance(result, bool) and not result:
            xbmcplugin.endOfDirectory(context.get_handle(), succeeded=False)
        elif isinstance(result, VideoItem) or isinstance(result, AudioItem):
            self._set_resolved_url(context, result)
        elif isinstance(result, DirectoryItem):
            self._add_directory(context, result)
        elif isinstance(result, list):
            item_count = len(result)
            for item in result:
                if isinstance(item, DirectoryItem):
                    self._add_directory(context, item, item_count)
                elif isinstance(item, VideoItem):
                    self._add_video(context, item, item_count)
                elif isinstance(item, AudioItem):
                    self._add_audio(context, item, item_count)
                elif isinstance(item, ImageItem):
                    self._add_image(context, item, item_count)
                pass

            xbmcplugin.endOfDirectory(
                context.get_handle(), succeeded=True,
                cacheToDisc=options.get(AbstractProvider.RESULT_CACHE_TO_DISC, True))

            # set alternative view mode
            if context.get_settings().is_override_view_enabled():
                view_mode = context.get_ui().get_view_mode()
                if view_mode is not None:
                    xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode)
                    pass
                pass
            pass
        else:
            # handle exception
            pass
        pass

    def _set_resolved_url(self, context, base_item, succeeded=True):
        list_item = xbmcgui.ListItem(path=base_item.get_uri())
        xbmcplugin.setResolvedUrl(context.get_handle(), succeeded=succeeded, listitem=list_item)

        """
        # just to be sure :)
        if not isLiveStream:
            tries = 100
            while tries>0:
                xbmc.sleep(50)
                if xbmc.Player().isPlaying() and xbmc.getCondVisibility("Player.Paused"):
                    xbmc.Player().pause()
                    break
                tries-=1
        """

    def _add_directory(self, context, directory_item, item_count=0):
        item = xbmcgui.ListItem(label=directory_item.get_name(),
                                iconImage=u'DefaultFolder.png',
                                thumbnailImage=directory_item.get_image())

        # only set fanart is enabled
        settings = context.get_settings()
        if directory_item.get_fanart() and settings.show_fanart():
            item.setProperty(u'fanart_image', directory_item.get_fanart())
            pass
        if directory_item.get_context_menu() is not None:
            item.addContextMenuItems(directory_item.get_context_menu())
            pass

        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=directory_item.get_uri(),
                                    listitem=item,
                                    isFolder=True,
                                    totalItems=item_count)
        pass

    def _add_video(self, context, video_item, item_count=0):
        item = xbmcgui.ListItem(label=video_item.get_name(),
                                iconImage=u'DefaultVideo.png',
                                thumbnailImage=video_item.get_image())

        # only set fanart is enabled
        settings = context.get_settings()
        if video_item.get_fanart() and settings.show_fanart():
            item.setProperty(u'fanart_image', video_item.get_fanart())
            pass
        if video_item.get_context_menu() is not None:
            item.addContextMenuItems(video_item.get_context_menu())
            pass

        item.setProperty(u'IsPlayable', u'true')

        item.setInfo(type=u'video', infoLabels=info_labels.create_from_item(video_item))

        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=video_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)
        pass

    def _add_image(self, context, image_item, item_count):
        item = xbmcgui.ListItem(label=image_item.get_name(),
                                iconImage=u'DefaultPicture.png',
                                thumbnailImage=image_item.get_image())

        # only set fanart is enabled
        settings = context.get_settings()
        if image_item.get_fanart() and settings.show_fanart():
            item.setProperty(u'fanart_image', image_item.get_fanart())
            pass
        if image_item.get_context_menu() is not None:
            item.addContextMenuItems(image_item.get_context_menu())
            pass

        item.setInfo(type=u'picture', infoLabels=info_labels.create_from_item(image_item))

        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=image_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)
        pass

    def _add_audio(self, context, audio_item, item_count):
        item = xbmcgui.ListItem(label=audio_item.get_name(),
                                iconImage=u'DefaultAudio.png',
                                thumbnailImage=audio_item.get_image())

        # only set fanart is enabled
        settings = context.get_settings()
        if audio_item.get_fanart() and settings.show_fanart():
            item.setProperty(u'fanart_image', audio_item.get_fanart())
            pass
        if audio_item.get_context_menu() is not None:
            item.addContextMenuItems(audio_item.get_context_menu())
            pass

        item.setProperty(u'IsPlayable', u'true')

        item.setInfo(type=u'music', infoLabels=info_labels.create_from_item(audio_item))

        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=audio_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)
        pass

    pass
