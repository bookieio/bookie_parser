<%inherit file="/wrapper.mako" />
<%def name="title()">Bookie: Error fetching content.</%def>
<div class="yui3-u-1">
    <h2>${error_message}</h2>
    <div>Upstream code: ${error_details['code']}</div>
</div>
