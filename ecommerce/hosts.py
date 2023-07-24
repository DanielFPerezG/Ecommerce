from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'danielperez', 'ecommerce.urls', name='www'),  # Dominio principal
    host(r'base', 'base.urls', name='base'),  # Subdominio base
)