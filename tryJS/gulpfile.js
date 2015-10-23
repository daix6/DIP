var gulp = require('gulp');
var $ = require('gulp-load-plugins')();

var http = require('http');
var st = require('st');
var path = require('path');

gulp.task('jade', function() {
  return gulp.src('./jade/*.jade')
    .pipe($.jade())
    .pipe(gulp.dest('./dist/'))
    .pipe($.livereload());
});

gulp.task('static', function() {
  return gulp.src(['./js/*', './css/*', './assets/*'])
    .pipe(gulp.dest('./dist/'))
    .pipe($.livereload());
});

gulp.task('watch', function () {
  $.livereload.listen({ basePath: 'dist' });
  gulp.watch('./jade/**/*.jade', ['jade']);
  gulp.watch('./js/*.js', ['static']);
  gulp.watch('./css/*.css', ['static']);
  gulp.watch('./assets/*', ['static']);
});

gulp.task('deploy', function() {
  return gulp.src('./dist/**/*')
    .pipe($.ghPages({
      branch: 'gh-pages'
    }));
});

function server(done) {
  http.createServer(
    st({
      path: __dirname + '/dist/',
      url: '/',
      index: '/index.html',
      cache: false
    })
  ).listen(8080, done);

  console.log('listening on http://localhost:8080');
}

gulp.task('default', ['jade', 'static', 'watch'], server);
