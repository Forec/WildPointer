
function verifyEmail(email) {
    var emailReg=/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/i;
    if (email.search(emailReg) == -1)
        return false;
    return true;
}

function verifyPassword(password) {
    if (password == "" || password.length < 8 || password.length > 22)
		return false;
	return true;
}

function verifyUsername(username) {
    var invalid = ['#', '@', '.', ',', '-', '$', '^', '&', '*', '\\', '/', '<', '>', '+', '='];
    for (var i = 0; i < invalid.length; i++) {
        if (username.indexOf(invalid[i]) != -1)
            return false;
    }
	if (username == "" || username.length < 5 || username.length > 32)
		return false;
	return true;
}

function verifyEmailOrUsername(seg) {
    if (seg.indexOf('@') != -1)
        return verifyEmail(seg);
    return verifyUsername(seg);
}