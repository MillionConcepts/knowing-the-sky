/* for jupyter 7, this needs to be built as an extension; custom.js is no longer supported */

// TODO: add load listener, something like:
//    define([
//        'base/js/namespace',
//        'base/js/promises'
//    ], function(IPython, promises) {
//        promises.app_initialized.then(styleDel)
// }

const transformToTooltip = function(element) {
    const splitter = /(?<text>.*?)\|(?<tooltip>.*)/
    const split =  element.innerText.match(splitter)
    if (split[1] === "") {
        return
    }
    // TODO: probably should be a <p> not a <div>, check
    //  inherited Markdown cell styles
    const wrapper = document.createElement('div')
    wrapper.classList.add('del-tooltip-wrapper')
    console.log(split)
    wrapper.innerText = split.groups.text
    const tooltip = document.createElement('span')
    tooltip.classList.add('del-tooltip-text')
    tooltip.innerText = split.groups.tooltip
    wrapper.appendChild(tooltip)
    element.parentNode.insertBefore(wrapper, element)
    element.remove()
}

const styleDel = function(_event) {
        let tooltips = document.getElementsByTagName('del')
    Array.from(tooltips).forEach(transformToTooltip)
}
