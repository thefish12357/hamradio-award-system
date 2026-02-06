// 奖状设计工具的JavaScript功能
let selectedElement = null;
let isDragging = false;
let isResizing = false;
let resizeStartX = 0;
let resizeStartY = 0;
let resizeStartW = 0;
let resizeStartH = 0;
let offsetX = 0;
let offsetY = 0;
let elements = [];
let elementCounter = 0;

// 初始化设计工具
function initDesignTool() {
    // 初始化背景
    document.getElementById('background-color').addEventListener('change', updateBackground);
    document.getElementById('background-upload').addEventListener('change', uploadBackgroundImage);
    
    // 初始化元素添加按钮
    document.getElementById('add-logo').addEventListener('click', () => addElement('logo'));
    document.getElementById('add-title').addEventListener('click', () => addElement('title'));
    document.getElementById('add-description').addEventListener('click', () => addElement('description'));
    document.getElementById('add-project').addEventListener('click', () => addElement('project'));
    document.getElementById('add-recipient').addEventListener('click', () => addElement('recipient'));
    document.getElementById('add-award-number').addEventListener('click', () => addElement('award-number'));
    document.getElementById('add-date').addEventListener('click', () => addElement('date'));
    document.getElementById('add-signer').addEventListener('click', () => addElement('signer'));
    
    // 初始化元素控制
    document.getElementById('element-text').addEventListener('input', updateElementText);
    document.getElementById('element-font').addEventListener('change', updateElementFont);
    document.getElementById('element-size').addEventListener('change', updateElementSize);
    document.getElementById('element-color').addEventListener('change', updateElementColor);
    document.getElementById('element-bold').addEventListener('change', updateElementBold);
    document.getElementById('element-italic').addEventListener('change', updateElementItalic);
    document.getElementById('element-underline').addEventListener('change', updateElementUnderline);
    
    // 初始化保存和预览按钮
    document.getElementById('save-template').addEventListener('click', saveTemplate);
    document.getElementById('preview-template').addEventListener('click', previewTemplate);

    // 模板文件与 logo 上传（用于保存到模板文件夹）
    const tplBgInput = document.getElementById('template-background');
    if (tplBgInput) tplBgInput.addEventListener('change', function(e){
        // 仅做预览（保存在 save 时上传）
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(ev){
                document.getElementById('award-canvas').style.backgroundImage = `url(${ev.target.result})`;
                document.getElementById('award-canvas').style.backgroundSize = 'cover';
            };
            reader.readAsDataURL(file);
        }
    });
    const tplLogoInput = document.getElementById('template-logo');
    if (tplLogoInput) tplLogoInput.addEventListener('change', function(e){
        // 不自动添加到画布，用户可以使用添加元素并手动设置图片路径
        console.log('模板 logo 已选择（保存时会上传）');
    });

    // 清除模板背景/Logo 的按钮
    const tplBgClear = document.getElementById('template-background-clear');
    if (tplBgClear) tplBgClear.addEventListener('click', function(){
        const inp = document.getElementById('template-background');
        if (inp) { inp.value = ''; }
        // 如果当前画布正显示该作为预览的 background-image，不修改画布预览（仅清除待上传文件）
        alert('已清除待上传的模板底图（预览不会回退）。如需清除画布上的背景，请使用画布左上角的背景颜色选择器或刷新页面。');
    });

    const tplLogoClear = document.getElementById('template-logo-clear');
    if (tplLogoClear) tplLogoClear.addEventListener('click', function(){
        const inp = document.getElementById('template-logo');
        if (inp) { inp.value = ''; }
        alert('已清除待上传的模板 Logo。');
    });
    
    // 初始化画布事件
    const canvas = document.getElementById('award-canvas');
    canvas.addEventListener('mousedown', onCanvasMouseDown);
    canvas.addEventListener('mousemove', onCanvasMouseMove);
    canvas.addEventListener('mouseup', onCanvasMouseUp);
    canvas.addEventListener('mouseleave', onCanvasMouseLeave);
    
    // 添加删除元素按钮
    const deleteButton = document.getElementById('delete-element');
    console.log('删除按钮元素:', deleteButton);
    deleteButton.addEventListener('click', deleteSelectedElement);
    // 同时添加键盘删除键支持
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Delete' || e.key === 'Backspace') {
            deleteSelectedElement();
        }
    });
}

// 更新背景颜色
function updateBackground() {
    const canvas = document.getElementById('award-canvas');
    const color = document.getElementById('background-color').value;
    canvas.style.backgroundColor = color;
}

// 上传背景图片
function uploadBackgroundImage(event) {
    const canvas = document.getElementById('award-canvas');
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        canvas.style.backgroundImage = `url(${e.target.result})`;
        canvas.style.backgroundSize = 'cover';
        canvas.style.backgroundPosition = 'center';
    };
    reader.readAsDataURL(file);
}

// 添加元素到画布
function addElement(type) {
    const canvas = document.getElementById('award-canvas');
    const element = document.createElement('div');
    element.id = `element-${elementCounter}`;
    element.className = 'draggable-element';
    
    // 设置初始文本
    let text = '';
    switch(type) {
        case 'logo':
            text = '';
            // 为 logo 提供默认尺寸（可以拖拽与缩放）
            element.dataset.width = '120';
            element.dataset.height = '120';
            element.style.width = '120px';
            element.style.height = '120px';
            break;
        case 'title':
            text = '奖状标题';
            break;
        case 'description':
            text = '奖状说明文字';
            break;
        case 'project':
            text = '奖状项目名称';
            break;
        case 'recipient':
            text = '领奖用户';
            break;
        case 'award-number':
            text = '奖状编号';
            break;
        case 'date':
            text = '生成日期';
            break;
        case 'signer':
            text = '签发人';
            break;
    }
    
    element.textContent = text;
    element.dataset.type = type;
    element.dataset.text = text;
    element.dataset.font = 'Arial';
    element.dataset.size = '16';
    element.dataset.color = '#000000';
    element.dataset.bold = 'false';
    element.dataset.italic = 'false';
    element.dataset.underline = 'false';
    
    // 随机位置
    const x = Math.random() * (canvas.offsetWidth - 150) + 10;
    const y = Math.random() * (canvas.offsetHeight - 50) + 10;
    element.style.left = x + 'px';
    element.style.top = y + 'px';
    
    // 设置初始样式
    updateElementStyle(element);
    
    // 添加事件监听器
    element.addEventListener('mousedown', onElementMouseDown);
    
    canvas.appendChild(element);
    elements.push({
        id: element.id,
        type: type,
        x: x,
        y: y,
        text: text,
        font: 'Arial',
        size: '16',
        color: '#000000',
        bold: false,
        italic: false,
        underline: false
    });
    
    // 选择新添加的元素
    selectElement(element);
    
    elementCounter++;
}

// 选中元素
function selectElement(element) {
    // 取消之前的选择
    if (selectedElement) {
        selectedElement.classList.remove('element-selected');
        selectedElement.dataset.selected = 'false';
    }
    
    // 选择新元素
    selectedElement = element;
    selectedElement.classList.add('element-selected');
    selectedElement.dataset.selected = 'true';
    
    // 更新控制面板
    document.getElementById('element-text').value = element.dataset.text;
    document.getElementById('element-font').value = element.dataset.font;
    document.getElementById('element-size').value = element.dataset.size;
    document.getElementById('element-color').value = element.dataset.color;
    document.getElementById('element-bold').checked = element.dataset.bold === 'true';
    document.getElementById('element-italic').checked = element.dataset.italic === 'true';
    document.getElementById('element-underline').checked = element.dataset.underline === 'true';
    
    // 显示控制面板
    document.getElementById('element-controls').style.display = 'block';
    // 如果是 logo 类型，显示图片上传控件
    const imgControl = document.getElementById('element-image-control');
    if (element.dataset.type === 'logo') {
        if (imgControl) imgControl.style.display = 'block';
        // 添加或显示缩放把手
        if (!element.querySelector('.resize-handle')) {
            const handle = document.createElement('div');
            handle.className = 'resize-handle';
            element.appendChild(handle);
            handle.addEventListener('mousedown', function(ev){
                ev.stopPropagation();
                isResizing = true;
                resizeStartX = ev.clientX;
                resizeStartY = ev.clientY;
                resizeStartW = parseInt(element.offsetWidth);
                resizeStartH = parseInt(element.offsetHeight);
                document.addEventListener('mousemove', onResizeMouseMove);
                document.addEventListener('mouseup', onResizeMouseUp);
            });
        }
    } else {
        if (imgControl) imgControl.style.display = 'none';
        // 移除可能存在的缩放把手
        const h = element.querySelector('.resize-handle');
        if (h) element.removeChild(h);
    }

    // 绑定元素图片上传事件（仅绑定一次）
    const imgUpload = document.getElementById('element-image-upload');
    if (imgUpload) {
        imgUpload.onchange = function(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(ev) {
                // 将图片添加为 selectedElement 的背景
                if (selectedElement) {
                    selectedElement.style.backgroundImage = `url(${ev.target.result})`;
                    selectedElement.style.backgroundSize = 'contain';
                    selectedElement.style.backgroundRepeat = 'no-repeat';
                    selectedElement.style.backgroundPosition = 'center';
                    // 记录在 dataset 中（仅临时预览）
                    selectedElement.dataset.image = ev.target.result;
                    // 同步 elements 数据（如果存在）
                    const idx = elements.findIndex(el => el.id === selectedElement.id);
                    if (idx !== -1) {
                        elements[idx].image = ev.target.result;
                    }
                }
            };
            reader.readAsDataURL(file);
        };
    }
}

// 元素鼠标按下事件
function onElementMouseDown(e) {
    e.stopPropagation();
    console.log('元素被点击:', this.id);
    selectedElement = this;
    isDragging = true;
    
    // 计算偏移量
    offsetX = e.clientX - parseInt(this.style.left);
    offsetY = e.clientY - parseInt(this.style.top);
    
    selectElement(this);
    console.log('selectedElement现在是:', selectedElement ? selectedElement.id : null);
    
    // 添加全局鼠标事件
    document.addEventListener('mousemove', onElementMouseMove);
    document.addEventListener('mouseup', onElementMouseUp);
}

// 元素鼠标移动事件
function onElementMouseMove(e) {
    if (!isDragging || !selectedElement || isResizing) return;
    
    const canvas = document.getElementById('award-canvas');
    const canvasRect = canvas.getBoundingClientRect();
    
    // 计算新位置 - 修复偏移问题：只使用相对于画布的偏移量
    let newX = e.clientX - canvasRect.left;
    let newY = e.clientY - canvasRect.top;
    
    // 限制在画布内
    newX = Math.max(0, Math.min(newX, canvas.offsetWidth - selectedElement.offsetWidth));
    newY = Math.max(0, Math.min(newY, canvas.offsetHeight - selectedElement.offsetHeight));
    
    // 更新元素位置
    selectedElement.style.left = newX + 'px';
    selectedElement.style.top = newY + 'px';
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].x = newX;
        elements[elementIndex].y = newY;
    }
}

// 缩放处理
function onResizeMouseMove(e) {
    if (!isResizing || !selectedElement) return;
    const dx = e.clientX - resizeStartX;
    const dy = e.clientY - resizeStartY;
    const newW = Math.max(10, resizeStartW + dx);
    const newH = Math.max(10, resizeStartH + dy);
    selectedElement.style.width = newW + 'px';
    selectedElement.style.height = newH + 'px';
    selectedElement.dataset.width = String(newW);
    selectedElement.dataset.height = String(newH);
    // 更新数据模型
    const idx = elements.findIndex(el => el.id === selectedElement.id);
    if (idx !== -1) {
        elements[idx].width = newW;
        elements[idx].height = newH;
    }
}

function onResizeMouseUp(e) {
    if (!isResizing) return;
    isResizing = false;
    document.removeEventListener('mousemove', onResizeMouseMove);
    document.removeEventListener('mouseup', onResizeMouseUp);
}

// 元素鼠标释放事件
function onElementMouseUp() {
    isDragging = false;
    document.removeEventListener('mousemove', onElementMouseMove);
    document.removeEventListener('mouseup', onElementMouseUp);
}

// 画布鼠标按下事件
function onCanvasMouseDown(e) {
    if (e.target === document.getElementById('award-canvas')) {
        // 点击画布空白处，取消选择
        if (selectedElement) {
            selectedElement.classList.remove('element-selected');
            selectedElement = null;
            document.getElementById('element-controls').style.display = 'none';
        }
    }
}

// 画布鼠标移动事件（委托给元素移动处理，避免未定义错误）
function onCanvasMouseMove(e) {
    if (isDragging && selectedElement) {
        onElementMouseMove(e);
    }
}

// 画布鼠标释放事件（停止拖拽）
function onCanvasMouseUp(e) {
    if (isDragging) {
        onElementMouseUp(e);
    }
}

// 鼠标移出画布时停止拖拽
function onCanvasMouseLeave(e) {
    if (isDragging) {
        onElementMouseUp(e);
    }
}

// 更新元素样式
function updateElementStyle(element) {
    const type = element.dataset.type;
    if (type === 'logo') {
        // logo 使用 width/height 数据来控制大小
        const w = element.dataset.width || element.style.width.replace('px','') || '120';
        const h = element.dataset.height || element.style.height.replace('px','') || '120';
        element.style.width = parseInt(w) + 'px';
        element.style.height = parseInt(h) + 'px';
        // 保持文本空
        element.textContent = '';
    } else {
        const font = element.dataset.font;
        const size = element.dataset.size;
        const color = element.dataset.color;
        const bold = element.dataset.bold === 'true' ? 'bold' : 'normal';
        const italic = element.dataset.italic === 'true' ? 'italic' : 'normal';
        const underline = element.dataset.underline === 'true' ? 'underline' : 'none';
        
        element.style.fontFamily = font;
        element.style.fontSize = size + 'px';
        element.style.color = color;
        element.style.fontWeight = bold;
        element.style.fontStyle = italic;
        element.style.textDecoration = underline;
    }
}

// 更新元素文本
function updateElementText() {
    if (!selectedElement) return;
    
    const text = document.getElementById('element-text').value;
    selectedElement.textContent = text;
    selectedElement.dataset.text = text;
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].text = text;
    }
}

// 更新元素字体
function updateElementFont() {
    if (!selectedElement) return;
    
    const font = document.getElementById('element-font').value;
    selectedElement.dataset.font = font;
    updateElementStyle(selectedElement);
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].font = font;
    }
}

// 更新元素大小
function updateElementSize() {
    if (!selectedElement) return;
    
    const size = document.getElementById('element-size').value;
    selectedElement.dataset.size = size;
    updateElementStyle(selectedElement);
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].size = size;
    }
}

// 更新元素颜色
function updateElementColor() {
    if (!selectedElement) return;
    
    const color = document.getElementById('element-color').value;
    selectedElement.dataset.color = color;
    updateElementStyle(selectedElement);
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].color = color;
    }
}

// 更新元素粗体
function updateElementBold() {
    if (!selectedElement) return;
    
    const bold = document.getElementById('element-bold').checked;
    selectedElement.dataset.bold = bold.toString();
    updateElementStyle(selectedElement);
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].bold = bold;
    }
}

// 更新元素斜体
function updateElementItalic() {
    if (!selectedElement) return;
    
    const italic = document.getElementById('element-italic').checked;
    selectedElement.dataset.italic = italic.toString();
    updateElementStyle(selectedElement);
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].italic = italic;
    }
}

// 更新元素下划线
function updateElementUnderline() {
    if (!selectedElement) return;
    
    const underline = document.getElementById('element-underline').checked;
    selectedElement.dataset.underline = underline.toString();
    updateElementStyle(selectedElement);
    
    // 更新元素数据
    const elementIndex = elements.findIndex(el => el.id === selectedElement.id);
    if (elementIndex !== -1) {
        elements[elementIndex].underline = underline;
    }
}

// 删除选中元素
function deleteSelectedElement() {
    console.log('删除按钮被点击');

    // 诊断信息
    console.log('当前 selectedElement 变量:', selectedElement);
    console.log('DOM 中的 .element-selected:', document.querySelector('.element-selected'));
    console.log('elements 数组长度:', elements.length);

    // 先检查 selectedElement
    let elementToDelete = selectedElement;

    // 如果 selectedElement 不存在，尝试在画布内查找标记或类
    if (!elementToDelete) {
        const canvas = document.getElementById('award-canvas');
        elementToDelete = canvas.querySelector('.element-selected') || canvas.querySelector('[data-selected="true"]') || document.querySelector('.element-selected');
        console.log('回退查找得到的元素:', elementToDelete);
    }

    if (!elementToDelete) {
        console.log('没有找到选中的元素，无法删除');
        alert('请先选择一个元素再删除');
        return;
    }

    // 确保我们拥有最新的 DOM 引用（防止引用丢失）
    if (!elementToDelete.parentNode && elementToDelete.id) {
        const byId = document.getElementById(elementToDelete.id);
        if (byId) {
            elementToDelete = byId;
            console.log('通过 id 恢复了元素引用:', elementToDelete);
        }
    }

    console.log('正在删除元素:', elementToDelete.id || elementToDelete);

    // 从画布中删除
    try {
        const canvas = document.getElementById('award-canvas');
        if (canvas && canvas.contains(elementToDelete)) {
            canvas.removeChild(elementToDelete);
            console.log('从画布移除成功');
        } else if (elementToDelete.parentNode) {
            elementToDelete.parentNode.removeChild(elementToDelete);
            console.log('从父节点移除成功');
        } else {
            console.warn('元素没有父节点，可能已被移除');
        }
    } catch (err) {
        console.error('删除元素时出错:', err);
    }

    // 从元素列表中删除（根据 id 匹配）
    if (elementToDelete.id) {
        const before = elements.length;
        elements = elements.filter(el => el.id !== elementToDelete.id);
        console.log(`elements 数组：移除前 ${before} -> 移除后 ${elements.length}`);
    } else {
        console.log('被删除元素没有 id，跳过 elements 数组同步');
    }

    // 重置选择状态
    if (selectedElement && selectedElement === elementToDelete) selectedElement = null;
    // 也移除任何画布上残留的选择标记
    const canvas = document.getElementById('award-canvas');
    const anySelected = canvas.querySelector('.element-selected');
    if (anySelected) {
        anySelected.classList.remove('element-selected');
        anySelected.dataset.selected = 'false';
    }
    // 移除可能存在的 resize handle
    if (selectedElement) {
        const rh = selectedElement.querySelector && selectedElement.querySelector('.resize-handle');
        if (rh && rh.parentNode) rh.parentNode.removeChild(rh);
    }
    document.getElementById('element-controls').style.display = 'none';
    console.log('删除完成');
}

// 保存模板
function saveTemplate() {
    // 弹出奖状选择弹窗（在弹窗中选择 award_code 并确认后执行实际保存）
    const overlay = document.getElementById('award-select-overlay');
    if (!overlay) {
        alert('无法找到奖状选择弹窗元素');
        return;
    }
    overlay.style.display = 'block';

    // 初始化搜索过滤
    const searchInput = document.getElementById('award-search');
    const select = document.getElementById('award-select');
    searchInput.value = '';
    searchInput.oninput = function() {
        const q = this.value.toLowerCase();
        for (let i=0;i<select.options.length;i++) {
            const opt = select.options[i];
            opt.style.display = (opt.text.toLowerCase().indexOf(q) !== -1) ? '' : 'none';
        }
    };

    // 取消逻辑
    document.getElementById('award-select-cancel').onclick = function(){
        overlay.style.display = 'none';
    };

    // 确认并保存逻辑
    document.getElementById('award-select-confirm').onclick = function(){
        const award_code = select.value;
        if (!award_code) { alert('请选择奖状代码'); return; }
        overlay.style.display = 'none';
        performSaveTemplate(award_code);
    };
}

// 执行实际的保存动作（上传 template JSON 以及可选的背景/Logo 文件）
function performSaveTemplate(award_code) {
    const canvas = document.getElementById('award-canvas');
    const background = {
        color: canvas.style.backgroundColor || '#ffffff',
        image: canvas.style.backgroundImage || ''
    };

    const template = {
        background: background,
        elements: elements,
        timestamp: new Date().toISOString()
    };

    const form = new FormData();
    form.append('award_code', award_code);
    form.append('template', JSON.stringify(template));

    const bgInput = document.getElementById('template-background');
    if (bgInput && bgInput.files && bgInput.files[0]) {
        form.append('background_file', bgInput.files[0]);
    }
    const logoInput = document.getElementById('template-logo');
    if (logoInput && logoInput.files && logoInput.files[0]) {
        form.append('logo_file', logoInput.files[0]);
    }

    fetch('/save_template', {
        method: 'POST',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('模板保存成功：' + data.award_code);
        } else {
            alert('模板保存失败：' + data.message);
        }
    })
    .catch(err => {
        alert('保存模板时出错：' + err.message);
    });
}

// 预览模板
function previewTemplate() {
    // 获取画布背景信息
    const canvas = document.getElementById('award-canvas');
    const background = {
        color: canvas.style.backgroundColor,
        image: canvas.style.backgroundImage
    };
    
    // 构建模板数据
    const template = {
        background: background,
        elements: elements
    };
    
    // 打开预览窗口
    const previewWindow = window.open('', '_blank');
    if (!previewWindow) {
        alert('请允许弹出窗口以预览奖状！');
        return;
    }
    
    // 构建预览HTML
    let html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>奖状预览</title>
            <style>
                body { margin: 20px; font-family: Arial, sans-serif; }
                #preview-canvas {
                    width: 800px;
                    height: 600px;
                    background-color: ${background.color};
                    ${background.image ? `background-image: ${background.image};` : ''}
                    background-size: cover;
                    background-position: center;
                    border: 2px solid #000;
                    position: relative;
                    margin: 0 auto;
                }
                .preview-element {
                    position: absolute;
                }
            </style>
        </head>
        <body>
            <h1>奖状预览</h1>
            <div id="preview-canvas">
    `;
    
    // 添加元素
    elements.forEach(element => {
        const style = `
            left: ${element.x}px;
            top: ${element.y}px;
            font-family: ${element.font};
            font-size: ${element.size}px;
            color: ${element.color};
            font-weight: ${element.bold ? 'bold' : 'normal'};
            font-style: ${element.italic ? 'italic' : 'normal'};
            text-decoration: ${element.underline ? 'underline' : 'none'};
        `;
        html += `<div class="preview-element" style="${style}">${element.text}</div>`;
    });
    
    // 关闭HTML
    html += `
            </div>
            <button onclick="window.print()">打印</button>
        </body>
        </html>
    `;
    
    // 在新窗口中显示预览
    previewWindow.document.write(html);
    previewWindow.document.close();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initDesignTool);