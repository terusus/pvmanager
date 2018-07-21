"""
The GenericMediaController and reusable media functionality.
"""

from pathlib import Path

from cement.core.controller import expose

from pvmanager.abstract_base_controller import AbstractBaseController



class GenericMediaController(AbstractBaseController):
  """
  This is an base class for common media operations.
  """


  class Meta:
    """The meta configuration options for this controllers."""
    stacked_on = 'media'
    arguments = [
      (['extra_arguments'], dict(action='store', nargs='*'))
    ]


  def __init__(self):
    AbstractBaseController.__init__(self)
    self.media_path = None


  def _setup(self, app_obj):
    """The default cement controller setup."""
    super(GenericMediaController, self)._setup(app_obj)

    self.media_path = Path(self.get_config('prefix')) / 'media' / self.Meta.label
    if not self.media_path.exists():
      app_obj.log.info('creating {} media path ({})'.format(self.Meta.label, self.media_path))
      self.media_path.mkdir(parents=True)


  def _render(self, result):
    print('  {}'.format(result))


  def _get_file_path(self, file_name):
    return self.media_path / file_name


  @expose(help='List all media.')
  def list(self):
    self.app.render(dict(data=self.media_path.iterdir()), "list.m")


  @expose(help='Delete a media file.')
  def delete(self):
    size = len(self.app.pargs.extra_arguments)
    if 1 > size:
      self.app.log.error('usage: ... delete <file name>')
      return

    media_name = self.app.pargs.extra_arguments[0]
    media_path = self._get_file_path(media_name)

    if not media_path.exists():
      return

    user_confirmation = input('Confirm delete command (yes/no): ')

    if 'yes' != user_confirmation:
      return

    self.app.log.info('deleting media file {}'.format(media_path))

    media_path.unlink()
