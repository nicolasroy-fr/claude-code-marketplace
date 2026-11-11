# React / TypeScript review points

Complements `checklist.md`; project config (`tsconfig`, ESLint) takes
precedence. Add your own conventions below.

## Common pitfalls

- `useEffect`: missing / wrong dependencies, effect used to derive state that
  could be computed during render, missing cleanup (listeners, timers,
  subscriptions, aborted fetches), race conditions on async calls.
- State: derived state stored instead of computed, mutation of state or props,
  stale closures in callbacks, `setState` with a value depending on the
  previous one without the functional form.
- Keys: array index as key on reorderable lists, unstable keys.
- Hooks called conditionally or in loops.
- Unnecessary `useMemo` / `useCallback` (or missing ones where identity matters
  for a memoized child or effect dependency).
- `dangerouslySetInnerHTML` or unsanitized URLs / HTML.
- Accessibility: interactive `div`s, missing labels / `alt`, no keyboard access,
  focus management in dialogs.

## TypeScript

- `any`, non-null assertions (`!`) and `as` casts hiding real type problems.
- Props typed explicitly; unions modelled so invalid states are unrepresentable.
- Unhandled `undefined` from indexed access, optional fields, API responses
  (are they validated at the boundary?).

## Tests

- <!-- your Vitest + Testing Library conventions -->

## Project conventions

- <!-- component / hook structure, Tailwind usage, file layout… -->
