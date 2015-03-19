var data = $.get('dgl-status.json');
data.done(fillPlayerTable).fail(networkError);
