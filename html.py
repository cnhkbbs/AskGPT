index = """<!DOCTYPE html>
<html>
	<head>
		<style>
			pre {
				background-color: black;
			}

			.tongyi-design-highlighter-header {
				display: none;
			}

			#content {
				font-size: 40px;
			}

			pre {
				font-size: 36px !important;
			}

			.linenumber {
				font-size: 36px !important;
			}
		</style>
	</head>
	<body>
		<div id="content">

		</div>
		<script>
			var currentHost = window.location.host;
			var ws = new WebSocket("ws://" + currentHost + "/ws");
			var content = document.getElementById('content');
			ws.onopen = function() {
				content.innerHTML = 'Waiting for server';
			};

			ws.onmessage = function(e) {
				var data = e.data;
				try {
					content.innerHTML = data;
				} catch (error) {
					content.innerHTML = 'Failed to decode data:' + error;
				}
			};

			ws.onerror = function() {
				content.innerHTML = 'There was an error with the WebSocket connection.';
			};

			ws.onclose = function() {
				content.innerHTML = 'The WebSocket connection was closed. Reflash to reconnect.'
			};
		</script>
	</body>
</html>"""
