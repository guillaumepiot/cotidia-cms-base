request = require('superagent')

API = {}

API.domain = 'API_ENDPOINT'

API.call = (type='get', url='/', data=null, auth=true, onSuccess=null, onError=null)->

    #
    # Create the request instance based on the type of request
    #

    url = "#{this.domain}#{url}"

    switch type
        when 'get'
            r = request.get(url)
        when 'post'
            r = request.post(url)
        when 'put'
            r = request.put(url)
        when 'patch'
            r = request.patch(url)
        when 'delete'
            r = request.del(url)
        else
            console.log "Request type #{type} is not supported"

    #
    # Set the headers
    #

    r.set('Content-Type', 'application/json')

    if auth
        r.set("Authorization", "Token #{ localStorage.token }")

    #
    # If we have a CSRF token on the page, then add it to the headers
    #
    if document.getElementsByName("csrfmiddlewaretoken").length > 0
        r.set("X-CSRFToken", document.getElementsByName("csrfmiddlewaretoken")[0].value)
        

    #
    # Add data if applicable
    #

    if data
        if type == 'get'
            r.query(data)
        else
            r.send(data)

    #
    # Form type
    #

    r.type('form')

    #
    # Set default callbacks
    #

    if not onSuccess
        onSuccess = (res)->
            console.log 'Success', res

    if not onError
        onError = (res)->
            console.log 'Error', res

    #
    # Send the request
    #

    r.end((err, res)->

        if res and res.status == 204
            onSuccess({})

        if res and res.status == 404
            alert 'The API url called does not exist'
            return

        if err and not res
            alert 'Connection error'
            return

        status = res.status
        type = status / 100 | 0
        data = res.body



        switch type
            when 2
                onSuccess(data)
            when 4
                onError(data)
            when 5
                alert('Server error')
                console.log 'Server error'
        )

module.exports = API