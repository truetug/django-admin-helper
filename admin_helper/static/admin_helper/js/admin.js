if (typeof Object.create !== "function") {
    Object.create = function (obj) {
        function F() {}
        F.prototype = obj;
        return new F();
    };
}

(function($){
    var Admin = {
        error: function () {
            if (window.console && window.console.error) {
                window.console.error.apply(console, arguments);
            }
        },
        log: function () {
            if (window.console && window.console.log && this.options.debug) {
                window.console.log.apply(console, arguments);
            }
        },
        init: function(options) {
            var self = this;

            self.options = $.extend(true, $.admin.defaults, options);
            self.userOptions = options;

            if(!self.el) {
                $.ajax({
                    url: self.options.initUrl,
                    method: 'get',
                    dataType: 'json'
                })
                    .success($.proxy($.admin.onInit, self))
            }

            self.log('Admin::Initialized', self.options);
            self.bindEvents();
        },
        bindEvents: function() {
            var self = this;

            $(document).on({
                keydown: function (event) {
                    var keyCode = event.keyCode || event.which,
                        is_modifier = function() {
                            var result = (self.options.modifiers.length) ? false : true;

                            for(var i in self.options.modifiers) {
                                var key = self.options.modifiers[i] + 'Key';
                                if (event[key]) {
                                    result = true;
                                    break;
                                }
                            }

                            return result;
                        },
                        is_visible = function(){
                            var result = null;

                            function calculate() {
                                return self.el && self.el.is(':visible')
                            }

                            if(result === null) result = calculate();
                            return result;
                        };

                    self.log('Admin::onKeyDown', event);

                    if ($.inArray(keyCode, self.options.keys) != -1 && is_modifier()) {
                        $.admin.onTrigger.call(self);
                        event.preventDefault();
                    }
                    else if(is_visible() && keyCode == 27) {
                        $.admin.hide.call(self);
                    }
                    else if(is_visible() && keyCode == 13) {
                        var link = self.el.find('.b-admin__item-link').eq(0);
                        if(link.length) window.location = link.attr('href');
                    }
                },
                'click': function(event) {
                    if(self.el) {
                        var target = $(event.target);
                        self.log('Admin::Click', target);
                        if(target.parents().index(self.el) == -1 && target[0] != self.el[0]) $.admin.hide.call(self);
                    }
                }
            });
        }
    };

    $.admin = function(options) {
        /**
         * Constructor
         * @type {Admin}
         */
        var admin = Object.create(Admin);
        admin.init(options);

        return admin
    };

    $.admin.defaults = {
        action: null,
        currentUsername: null,
        currentFullname: null,
        originalUsername: null,

        logPrefix: 'Admin',
        keys: [192, 220],
        modifiers: ['ctrl', 'meta'],
        debug: false,
        source: null,
        minQuery: 3,
        timeout: 300
    };

    $.admin.hide = function() {
        var self = this;

        if(self.el.length) {
            self.el.removeClass('b-admin_active');
        }
    };

    $.admin.show = function() {
        var self = this;

        if(self.el) {
            self.el.addClass('b-admin_active');
            self.input.focus();
        }
    };

    $.admin.onInputChange = function(event) {
        var self = this,
            query = $(event.target).val();

        if(query.length < self.options.minQuery || query == self.query) return;
        self.log('Admin::onInputChange', event);

        clearTimeout(self.timeout);
        self.timeout = setTimeout(function(){
            self.query = query;
            self.container.html('');

            $.ajax({
                url: self.options.suggestUrl,
                data: {meta_name: query},
                method: 'get',
                dataType: 'json'
            })
                .success($.proxy($.admin.onSuccessSuggest, self))
        }, self.options.timeout);
    };

    $.admin.onSuccessSuggest = function(response){
        var self = this;
        self.log('Admin::SuggestSuccess', response);
        self.container.html(response.data);
    };

    $.admin.onTrigger = function(){
        var self = this,
            func = self.el && (self.el.is(':visible')) ? $.admin.hide : $.admin.show;

        self.log('Admin::onTrigger');
        if(func) func.call(self);
    };

    $.admin.onInit = function(response){
        var self = this;
        self.log('Admin::onTrigger');

        self.el = $(response.data);
        self.container = self.el.find('.b-admin__container');
        self.input = self.el.find('.b-admin__input')
            .addClass('b-admin__input')
            .on('keyup', $.proxy($.admin.onInputChange, self));

        $('body').append(self.el);
    };

    $.admin({
        //debug: true,
        suggestUrl: $('meta[name="admin-suggest-url"]').attr('content'),
        initUrl: $('meta[name="admin-init-url"]').attr('content'),
        currentUsername: $('meta[name="admin-current-username"]').attr('content'),
        currentFullname: $('meta[name="admin-current-fullname"]').attr('content'),
        originalUsername: $('meta[name="admin-original-username"]').attr('content')
    });

})(jQuery);