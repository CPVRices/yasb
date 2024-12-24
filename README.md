[Original README](https://github.com/amnweb/yasb/blob/main/README.md)

This fork is customized to fit @scarlaid's needs.

## Openkey Widget

Widget YAML code:
```yaml
  openkey:
    type: "yasb.open_key.OpenKeyWidget"
    options:
      label: "lang: %l"
      update_interval: 50
```

Widget CSS:
```css
.openkey-widget {
    background-color: #1e1e2e;
    padding: 0 -2px 0 -2px
}
.openkey-widget .icon {
    color: #142123;
    padding: 0 6px;
}
.openkey-widget .label {
    background-color: #1e1e2e;
    color: #f5c276;
    padding: 0 8px;
    margin: 0px;
    border-radius: 6px;
}
```