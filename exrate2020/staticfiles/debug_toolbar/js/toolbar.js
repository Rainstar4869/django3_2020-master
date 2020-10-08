import { $$, ajax } from "./utils.js";

const onKeyDown = function (event) {
    if (event.keyCode === 27) {
        djdt.hide_one_level();
    }
};

const djdt = {
    handleDragged: false,
    init: function () {
        const djDebug = document.querySelector("#djDebug");
        $$.show(djDebug);
        $$.on(
            djDebug.querySelector("#djDebugPanelList"),
            "click",
            "li a",
            function (event) {
                event.preventDefault();
                if (!this.className) {
                    return;
                }
                const current = djDebug.querySelector("#" + this.className);
                if ($$.visible(current)) {
                    djdt.hide_panels();
                } else {
                    djdt.hide_panels();

                    $$.show(current);
                    this.parentElement.classList.add("djdt-active");

                    const inner = current.querySelector(
                            ".djDebugPanelContent .djdt-scroll"
                        ),
                        store_id = djDebug.dataset.storeId;
                    if (store_id && inner.children.length === 0) {
                        const url = new URL(
                            djDebug.dataset.renderPanelUrl,
                            window.location
                        );
                        url.searchParams.append("store_id", store_id);
                        url.searchParams.append("panel_id", this.className);
                        ajax(url).then(function (data) {
                            inner.previousElementSibling.remove(); // Remove AJAX loader
                            inner.innerHTML = data.content;
                            $$.executeScripts(data.scripts);
                        });
                    }
                }
            }
        );
        $$.on(djDebug, "click", ".djDebugClose", function () {
            djdt.hide_one_level();
        });
        $$.on(
            djDebug,
            "click",
            ".djDebugPanelButton input[type=checkbox]",
            function () {
                djdt.cookie.set(
                    this.dataset.cookie,
                    this.checked ? "on" : "off",
                    {
                        path: "/",
                        expires: 10,
                    }
                );
            }
        );

        // Used by the SQL and template panels
        $$.on(djDebug, "click", ".remoteCall", function (event) {
            event.preventDefault();

            let url;
            const ajax_data = {};

            if (this.tagName === "BUTTON") {
                const form = this.closest("form");
                url = this.formAction;
                ajax_data.method = form.method.toUpperCase();
                ajax_data.body = new FormData(form);
            } else if (this.tagName === "A") {
                url = this.href;
            }

            ajax(url, ajax_data).then(function (data) {
                const win = djDebug.querySelector("#djDebugWindow");
                win.innerHTML = data.content;
                $$.show(win);
            });
        });

        // Used by the cache, profiling and SQL panels
        $$.on(djDebug, "click", ".djToggleSwitch", function () {
            const id = this.dataset.toggleId;
            const toggleOpen = "+";
            const toggleClose = "-";
            const open_me = this.textContent === toggleOpen;
            const name = this.dataset.toggleName;
            const container = this.closest(
                ".djDebugPanelContent"
            ).querySelector("#" + name + "_" + id);
            container
                .querySelectorAll(".djDebugCollapsed")
                .forEach(function (e) {
                    $$.toggle(e, open_me);
                });
            container
                .querySelectorAll(".djDebugUncollapsed")
                .forEach(function (e) {
                    $$.toggle(e, !open_me);
                });
            const self = this;
            this.closest(".djDebugPanelContent")
                .querySelectorAll(".djToggleDetails_" + id)
                .forEach(function (e) {
                    if (open_me) {
                        e.classList.add("djSelected");
                        e.classList.remove("djUnselected");
                        self.textContent = toggleClose;
                    } else {
                        e.classList.remove("djSelected");
                        e.classList.add("djUnselected");
                        self.textContent = toggleOpen;
                    }
                    const switch_ = e.querySelector(".djToggleSwitch");
                    if (switch_) {
                        switch_.textContent = self.textContent;
                    }
                });
        });

        djDebug
            .querySelector("#djHideToolBarButton")
            .addEventListener("click", function (event) {
                event.preventDefault();
                djdt.hide_toolbar(true);
            });
        djDebug
            .querySelector("#djShowToolBarButton")
            .addEventListener("click", function () {
                if (!djdt.handleDragged) {
                    djdt.show_toolbar();
                }
            });
        let startPageY, baseY;
        const handle = document.querySelector("#djDebugToolbarHandle");
        const onHandleMove = function (event) {
            // Chrome can send spurious mousemove events, so don't do anything unless the
            // cursor really moved.  Otherwise, it will be impossible to expand the toolbar
            // due to djdt.handleDragged being set to true.
            if (djdt.handleDragged || event.pageY !== startPageY) {
                let top = baseY + event.pageY;

                if (top < 0) {
                    top = 0;
                } else if (top + handle.offsetHeight > window.innerHeight) {
                    top = window.innerHeight - handle.offsetHeight;
                }

                handle.style.top = top + "px";
                djdt.handleDragged = true;
            }
        };
        djDebug
            .querySelector("#djShowToolBarButton")
            .addEventListener("mousedown", function (event) {
                event.preventDefault();
                startPageY = event.pageY;
                baseY = handle.offsetTop - startPageY;
                document.addEventListener("mousemove", onHandleMove);
            });
        document.addEventListener("mouseup", function (event) {
            document.removeEventListener("mousemove", onHandleMove);
            if (djdt.handleDragged) {
                event.preventDefault();
                localStorage.setItem("djdt.top", handle.offsetTop);
                requestAnimationFrame(function () {
                    djdt.handleDragged = false;
                });
            }
        });
        const show =
            localStorage.getItem("djdt.show") || djDebug.dataset.defaultShow;
        if (show === "true") {
            djdt.show_toolbar();
        } else {
            djdt.hide_toolbar();
        }
    },
    hide_panels: function () {
        const djDebug = document.getElementById("djDebug");
        $$.hide(djDebug.querySelector("#djDebugWindow"));
        djDebug.querySelectorAll(".djdt-panelContent").forEach(function (e) {
            $$.hide(e);
        });
        djDebug.querySelectorAll("#djDebugToolbar li").forEach(function (e) {
            e.classList.remove("djdt-active");
        });
    },
    hide_toolbar: function () {
        djdt.hide_panels();

        const djDebug = document.getElementById("djDebug");
        $$.hide(djDebug.querySelector("#djDebugToolbar"));

        const handle = document.querySelector("#djDebugToolbarHandle");
        $$.show(handle);
        // set handle position
        let handleTop = localStorage.getItem("djdt.top");
        if (handleTop) {
            handleTop = Math.min(
                handleTop,
                window.innerHeight - handle.offsetHeight
            );
            handle.style.top = handleTop + "px";
        }

        document.removeEventListener("keydown", onKeyDown);

        localStorage.setItem("djdt.show", "false");
    },
    hide_one_level: function () {
        const djDebug = document.getElementById("djDebug");
        if ($$.visible(djDebug.querySelector("#djDebugWindow"))) {
            $$.hide(djDebug.querySelector("#djDebugWindow"));
        } else if (djDebug.querySelector("#djDebugToolbar li.djdt-active")) {
            djdt.hide_panels();
        } else {
            djdt.hide_toolbar(true);
        }
    },
    show_toolbar: function () {
        document.addEventListener("keydown", onKeyDown);
        const djDebug = document.getElementById("djDebug");
        $$.hide(djDebug.querySelector("#djDebugToolbarHandle"));
        $$.show(djDebug.querySelector("#djDebugToolbar"));
        localStorage.setItem("djdt.show", "true");
    },
    cookie: {
        get: function (key) {
            if (document.cookie.indexOf(key) === -1) {
                return null;
            }

            const cookieArray = document.cookie.split("; "),
                cookies = {};

            cookieArray.forEach(function (e) {
                const parts = e.split("=");
                cookies[parts[0]] = parts[1];
            });

            return cookies[key];
        },
        set: function (key, value, options) {
            options = options || {};

            if (typeof options.expires === "number") {
                const days = options.expires,
                    t = (options.expires = new Date());
                t.setDate(t.getDate() + days);
            }

            document.cookie = [
                encodeURIComponent(key) + "=" + String(value),
                options.expires
                    ? "; expires=" + options.expires.toUTCString()
                    : "",
                options.path ? "; path=" + options.path : "",
                options.domain ? "; domain=" + options.domain : "",
                options.secure ? "; secure" : "",
            ].join("");

            return value;
        },
    },
};
window.djdt = {
    show_toolbar: djdt.show_toolbar,
    hide_toolbar: djdt.hide_toolbar,
    init: djdt.init,
    close: djdt.hide_one_level,
    cookie: djdt.cookie,
};

if (document.readyState !== "loading") {
    djdt.init();
} else {
    document.addEventListener("DOMContentLoaded", djdt.init);
}