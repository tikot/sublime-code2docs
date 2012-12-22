import sublime, sublime_plugin
import subprocess, os, platform

class gendocCommand(sublime_plugin.TextCommand):
   def run(self, edit):
      localview = self.view
      self_file = self.view.file_name()

      settings = sublime.load_settings('Code2Docs.sublime-settings')
      
      output = localview.settings().get('output_path', settings.get('output_path'))
      css = localview.settings().get('css_file', settings.get('css_file'))
      template = localview.settings().get('template_file', settings.get('template_file'))
      
      fileDir(self_file, output, css, template)
   
def fileDir(self_file, output, css, template):

   if output == './':
      its_dir = os.path.dirname(self_file)
   else:
      its_dir = os.path.dirname(output)

   window = sublime.active_window()
   folders = window.folders()
   for folder in folders:
      if self_file.startswith(folder):
         its_dir = folder
         break
      else:
         its_dir = os.path.dirname(self_file)

   output = os.path.normpath(its_dir)

   return generateDocs(file_to_doc = self_file, css = css, template = template, doc_dir = output)

def generateDocs(file_to_doc, css, template, doc_dir):

   cmd = ['docco', file_to_doc]

   if platform.system() == 'Windows':
      cmd[0] = 'docco.cmd'

   if css != "":
      cmd.extend(['-c', css])

   if template != "":
      cmd.extend(['-t', template])

   p = subprocess.Popen(cmd, cwd = doc_dir, shell = False)