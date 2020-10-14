from django.test import TestCase


tag_info = {'<h\d>': '',
            '</h\d>': '<br>',
            '<script.*</script>': '',
            '<meta.*?>': '',
            '<link.*?>': ''
            }

for k, v in tag_info.items():
	print("k: ", k, "v: ", v)
	
	
print("-------")
for k in tag_info:
	print(k)