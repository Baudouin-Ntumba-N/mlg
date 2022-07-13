from django import template

register = template.Library()


def sizify(value):
    """
    Simple kb/mb/gb size snippet for templates:

    {{ product.file.size|sizify }}
    """
    #value = ing(value)
    if value < 512000:
        value = value / 1024.0
        ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'Mb'
    else:
        value = value / 1073741824.0
        ext = 'Gb'
    return '%s %s' % (str(round(value, 2)), ext)



def get_file_ext(file):

  file_name = file.name
  the_format = ""
  a=""
  j=0
  for i in file_name :
    j=j+1
    a=file_name[-j]
    if a == ".":
      break
    the_format = a + the_format
  file_format = the_format
  return file_format






register.filter('sizify', sizify)

register.filter('get_file_ext', get_file_ext)