const gulp = require('gulp');
const browserify = require('browserify');
const eslint = require('gulp-eslint');
const uglify = require('gulp-uglify');
const source = require('vinyl-source-stream');
const babelify = require('babelify');
const reactify = require('reactify');
const sourcemaps = require('gulp-sourcemaps');
var buffer = require('vinyl-buffer');

gulp.task('scripts', () => {
  const b = browserify({
    entries: './client/src/main.js',
    debug: true,
  })
  .transform(babelify.configure({
    presets: ['react', 'es2015'],
  }))
  .transform(reactify, {
  });

  b.bundle()
    .on('error', (err) => {
      console.log(err);
    })
    .pipe(source('app.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('client/build/js'));
});

gulp.task('lint', () => {
  gulp.src(['client/src/**/*.js'])
    .pipe(eslint())
    .pipe(eslint.format());
});

gulp.task('watch', () => {
  gulp.watch(['./client/src/**'], ['scripts', 'lint']);
});

gulp.task('default', ['scripts', 'lint', 'watch']);
