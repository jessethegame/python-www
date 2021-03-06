NONE = set()
ALL = set(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'OPTIONS'])
IDEMPOTENT = ALL - set(['POST', 'PATCH'])
SAFE = IDEMPOTENT - set(['PUT', 'DELETE'])
DANGEROUS = ALL - SAFE
FORM = set(['GET', 'POST'])
DATA = set(['PUT', 'POST', 'PATCH'])

