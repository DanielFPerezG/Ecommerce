from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'ecommerce.urls', name=' '),
    host(r'base', 'base.urls', name='base'),
)