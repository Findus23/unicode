export function navigate(to: string) {
    history.pushState({}, "", to)
    dispatchEvent(new CustomEvent("app:navigate", {detail: {to}}))
}
