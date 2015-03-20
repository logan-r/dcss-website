module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    htmlmin: {
      build: {
        options: {
          removeComments: true,
          collapseWhitespace: true
        },
        files: {
          '_site/index.html': '_site/index.html',
          '_site/download.html': '_site/download.html',
          '_site/play.html': '_site/play.html',
          '_site/watch.html': '_site/watch.html'
        }
      }
    },
    uglify: {
      build: {
        files: [{
          expand: true,
          cwd: '_site/js',
          src: '*.js',
          dest: '_site/js'
      }]
      }
    },
    template: {
      build: {
        'options': {
          'data': {
            'baseurl': 'https://www.dcssgame.com'
          }
        },
        files: {
          '_site/index.html': '_site/index.html',
          '_site/download.html': '_site/download.html',
          '_site/play.html': '_site/play.html',
          '_site/watch.html': '_site/watch.html'
        }
      }

    }
  });

  grunt.loadNpmTasks('grunt-contrib-htmlmin');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-template');

  grunt.registerTask('default', ['htmlmin', 'uglify', 'template']);

};
