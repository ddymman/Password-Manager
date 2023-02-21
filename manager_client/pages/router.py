from typing import TypedDict, Protocol
from manager_client.pages.route import Route


class RouteDict(TypedDict):
    route_name: str
    route: Route

# Allows for easy page-switching
# Also remembers previous pages to allow back-button functionality
class Router:
    def set_routes(self, routes: RouteDict, default_route: str):
        self.routes = routes
        self.route_stack = []
        self.default_route = default_route
        self.navigate_to(default_route)

    def hide_routes(self):
        for route in self.routes.values():
            route.hide()

    def navigate_to(self, route_name: str):
        self.hide_routes()

        route = self.routes.get(route_name)
        self.route_stack.append(route)
        route.show()

    def reset(self):
        self.route_stack.clear()
        self.navigate_to(self.default_route)

    def navigate_pop(self, route_name: str):
        try:
            self.route_stack.pop()
        except IndexError:
            pass

        self.navigate_to(route_name)

    def navigate_back(self):
        try:
            self.route_stack.pop()
        except IndexError:
            pass

        route = self.route_stack[-1]
        if route is not None:
            self.hide_routes()
            route.show()
