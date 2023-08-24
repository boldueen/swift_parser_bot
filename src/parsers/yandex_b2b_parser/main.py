

print('writing a file in volume', flush=True)
with open('/data/test_file.txt', 'w') as f:
    f.write('common buddy u must work')
print('file was written!', flush=True)
