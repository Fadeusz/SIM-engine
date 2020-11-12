function ajax (url, callback) {
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			console.log(xhr.response);
			callback(xhr.response)
		}
	}
	xhr.open('GET', url, true);
	xhr.send('');
}