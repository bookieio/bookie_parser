<h3>Urls: ${len(urls)} -- Refs: ${len(refs)}</h3>
<dl>
% for url in urls.values():
    <dt id="${url.get('hash_id')}">
        <a href="/u/${url.get('hash_id')}" title="View readable contents.">${url.get('hash_id')}</a>
        <dd>
            <a href="${url.get('url')}" title="Load original page.">${url.get('url')}</a>
        </dd>
    </dt>
% endfor

    <dt>References
        % for ref in refs:
            <dd>
                <a href="#${ref}">${ref}</a>
            </dd>
        % endfor
    </dt>
</dl>
