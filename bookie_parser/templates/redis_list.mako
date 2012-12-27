<ul>
% for url in urls:
    % if not 'reference' in url:
        <li>${url.get('hash_id')}: ${url.get('url')}</li>
    % else:
        <li>Reference: ${url.get('reference')}</li>
    % endif
% endfor
</ul>
