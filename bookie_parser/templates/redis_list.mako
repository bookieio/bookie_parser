<h3>Count: ${count}</h3>
<dl>
% for url in urls.values():
    <dt id="${url.get('hash_id')}"> ${url.get('hash_id')}</dt>
        <dd>
            <a href="${url.get('url')}">${url.get('url')}</a>
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
