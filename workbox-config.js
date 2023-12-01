module.exports = {
	globDirectory: '_site/',
	globPatterns: [
		'**/*.{html,css,xml,png,jpeg,js,json}'
	],
	swDest: '_site/sw.js',
	ignoreURLParametersMatching: [
		/^utm_/,
		/^fbclid$/
	]
};
