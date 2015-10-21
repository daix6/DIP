var gulp = require('gulp');
var $ = require('gulp-load-plugins')();

var http = require('http');
var st = require('st');
var path = require('path');

gulp.task('watch', function () {
  $.livereload.listen({ basePath: '.' });
  gulp.watch('**/*.html', []);
  gulp.watch('**/*.css', []);
  gulp.watch('**/*.js', []);
});

gulp.task('deploy', function() {
  return gulp.src(['./hw*/**/*', 'index.*', 'assets/*'])
    .pipe($.ghPages({
      branch: 'gh-pages',
      message: 'test server'
    }));
});

function server(done) {
  http.createServer(
    st({
      path: __dirname,
      url: '/',
      index: '/index.html',
      cache: false,
      dot:true
    })
  ).listen(8080, done);
  console.log('listening on http://localhost:8080');
}

gulp.task('default', server);
