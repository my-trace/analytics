const gulp = require('gulp');
// const browserify = require('gulp-browserify');
var browserify = require('browserify');
const eslint = require('gulp-eslint');
var uglify = require('gulp-uglify');
var source = require('vinyl-source-stream');
var babelify = require('babelify');
var reactify = require('reactify')
var buffer = require('vinyl-buffer');

// Basic usage
gulp.task('scripts', () => {
    // Single entry point to browserify
    var b = browserify({
      entries: './client/src/main.js',
      debug: true,
    })
    .transform(babelify.configure({
      presets: ['react', 'es2015'],
    }))
    .transform(reactify);

    b.bundle()
	.on('error', (err) => {
		console.log(err)
		// this.emit('end');
	})
	.pipe(source('app.js'))
	.pipe(gulp.dest('client/build/js'));
});

gulp.task('lint', () => {
	gulp.src(['client/src/**/*.js'])
    	.pipe(eslint())
    	.pipe(eslint.format());
});

gulp.task('watch', () => {
	gulp.watch(['./client/src/**'],['scripts']);
});

gulp.task('default', ['scripts', 'lint', 'watch']);