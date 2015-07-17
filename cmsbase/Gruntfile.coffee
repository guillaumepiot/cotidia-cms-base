module.exports = (grunt) ->

    # Project configuration
    grunt.initConfig({

        pkg: grunt.file.readJSON('package.json')

        coffee:
            options:
                join: true

            sandbox:
                files:
                    'static/admin/js/sandbox.js': [
                        'www/scripts/image-uploader.coffee'
                        'www/scripts/sandbox.coffee'
                        ]

        browserify:
            dist:
                options:
                    transform: ['coffee-reactify']
                files:
                    'static/admin/js/sandbox.js': ['www/scripts/sandbox.coffee']

        sass:
            sandbox:
                files:
                    'static/admin/css/sandbox.css': 'www/styles/sandbox.scss'

        uglify:
            options:
                banner: '/*! <%= pkg.name %> v<%= pkg.version %> by <%= pkg.author.name %> <<%= pkg.author.email %>> (<%= pkg.author.url %>) */\n'
                mangle: false

            build:
                src: 'build/content-tools.js'
                dest: 'build/content-tools.min.js'

        'string-replace': {    
            dev: {             
                files: {
                    "static/admin/js/sandbox.js": "static/admin/js/sandbox.js"
                },
                options: {
                    replacements: [{
                        pattern: /API_ENDPOINT/g,
                        replacement: "/"
                    }]
                }
            }
        }

        clean:
            build: ['src/tmp']

        watch:
            sandbox:
                files: [
                    'www/scripts/*.coffee',
                    'www/styles/*.scss'
                    ]
                tasks: ['sandbox']
    })

    # Plug-ins
    grunt.loadNpmTasks 'grunt-contrib-clean'
    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-concat'
    grunt.loadNpmTasks 'grunt-contrib-sass'
    grunt.loadNpmTasks 'grunt-contrib-uglify'
    grunt.loadNpmTasks 'grunt-contrib-watch'
    grunt.loadNpmTasks 'grunt-browserify'
    grunt.loadNpmTasks 'grunt-coffee-react'
    grunt.loadNpmTasks 'grunt-string-replace'

    # Tasks
    grunt.registerTask 'sandbox', [
        'browserify'
        'string-replace'
        #'coffee:sandbox'
        # 'sass:sandbox'
    ]

    grunt.registerTask 'watch-sandbox', ['watch:sandbox']