
namespace test {
    export function foo() {
        // @ts-ignore
        if (typeof control !== "undefined") return 1;
        return 0;
    }
}
