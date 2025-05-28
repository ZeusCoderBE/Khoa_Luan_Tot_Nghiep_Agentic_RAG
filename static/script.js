// Hàm thao tác với sidebar
function toggleSidebar() {
    const $sidebar = $('.sidebar');
    const $toggleButton = $('.toggle-button');
    const $newChat = $('#new-chat');
    if ($sidebar.hasClass('sidebar-collapsed')) {
        $sidebar.removeClass('sidebar-collapsed');
        $('.sidebar-content').show();
        $toggleButton.attr('title', 'Close Sidebar');
        $newChat.attr('title', 'New Chat');
    } else {
        $sidebar.addClass('sidebar-collapsed');
        $('.sidebar-content').hide();
        $toggleButton.attr('title', 'Open Sidebar');
        $newChat.removeAttr('title');
    }
}

// Đặt title đúng trạng thái khi load trang
$(document).ready(function() {
    const $sidebar = $('.sidebar');
    const $toggleButton = $('.toggle-button');
    const $newChat = $('#new-chat');
    if ($sidebar.hasClass('sidebar-collapsed')) {
        $toggleButton.attr('title', 'Open Sidebar');
        $newChat.removeAttr('title');
    } else {
        $toggleButton.attr('title', 'Close Sidebar');
        $newChat.attr('title', 'New Chat');
    }
    updateSearchWebButtonState();
});

const $userInput = $('#user-query');
const $sendButton = $('#send-button');
let isLoading = false; // Trạng thái khi chatbot đang xử lý phản hồi
let isTyping = false;  // Trạng thái khi chatbot đang in từng từ của câu trả lời

// Kiểm tra nội dung của input-area để bật/tắt nút Send
$userInput.on('input', function() {
    updateSendButtonState(); // Cập nhật trạng thái nút Send khi người dùng nhập liệu
});

function updateSendButtonState() {
    // Chỉ kích hoạt nút Send nếu có ký tự trong input, chatbot không đang gõ và không đang chờ phản hồi
    if ($userInput.val().trim() !== "" && !isTyping && !isLoading) {
        $sendButton.addClass('active').removeClass('disabled').prop('disabled', false);
    } else {
        $sendButton.removeClass('active').addClass('disabled').prop('disabled', true);
    }
}

// Logic event khi user click button Send
$('#send-button').on('click', sendMessage);

// Logic event khi user ấn nút Enter thay thì button Send
$('#user-query').on('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

// Thêm biến trạng thái chế độ Search Web
let isSearchWebMode = false;

// Hàm cập nhật trạng thái nút Search Web
function updateSearchWebButtonState() {
    if (currentSessionId) {
        $('#toggle-search-web').prop('disabled', false).removeClass('disabled');
    } else {
        $('#toggle-search-web').prop('disabled', true).addClass('disabled');
    }
}

// Xử lý sự kiện click cho nút Search Web
$('#toggle-search-web').on('click', function() {
    if ($(this).prop('disabled')) return;
    console.log('Đã click Search Web!');
    isSearchWebMode = !isSearchWebMode;
    $(this).toggleClass('active', isSearchWebMode);
    if (isSearchWebMode) {
        $(this).find('span').text('🌐 Search');
        $('#user-query').attr('placeholder', 'Trả lời dùng Search Tool ...');
    } else {
        $(this).find('span').text('Chat');
        $('#user-query').attr('placeholder', 'Nhập tin nhắn ...');
    }
});

// Hàm gửi tin nhắn từ user
function sendMessage() {
    const query = $userInput.val().trim();
    if (!query || isLoading || isTyping) return;

    // Xóa nội dung của relevant-documents-container
    $('#relevant-documents-container').empty();

    $sendButton.prop('disabled', true).removeClass('active').addClass('disabled');
    isLoading = true;
    $('#loading-indicator').text("Loading...");

    const $chatOutput = $('#chat-output');
    $chatOutput.append(`
        <div class="chat-message user">
            <div class="avatar user-avatar" style="background-image: url('https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o=');"></div>
            <div class="message">${query}</div>
        </div>
    `);

    // Lưu tin nhắn của người dùng vào database
    saveMessage(currentSessionId, 'user', query);

    // Kiểm tra và thêm phiên chat vào sidebar nếu là tin nhắn đầu tiên
    if ($('#chat-sessions .chat-session[data-session-id="' + currentSessionId + '"]').length === 0) {
        addChatSessionToSidebar(currentSessionId, query);
    }

    $userInput.val('');
    $chatOutput.scrollTop($chatOutput.prop('scrollHeight'));

    const $typingIndicator = $(`
        <div class="chat-message bot typing-indicator">
            <div class="avatar bot-avatar" style="background-image: url('https://media.istockphoto.com/id/1333838449/vector/chatbot-icon-support-bot-cute-smiling-robot-with-headset-the-symbol-of-an-instant-response.jpg?s=612x612&w=0&k=20&c=sJ_uGp9wJ5SRsFYKPwb-dWQqkskfs7Fz5vCs2w5w950=');"></div>
            <div class="message" style="font-size: 14px;
                                color: rgba(0, 0, 0, 0.6); 
                                display: flex;
                                align-items: center;">
                Đang suy nghĩ câu trả lời 
                <div class="time-count" style="margin-left: 5px; margin-right: 5px;">
                00:00</div>
                <span>.</span><span>.</span><span>.</span>
            </div>
        </div>
    `);
    $chatOutput.append($typingIndicator);
    $chatOutput.scrollTop($chatOutput.prop('scrollHeight'));

    // Khởi tạo thời gian bắt đầu
    const startTime = Date.now();

    // Cập nhật số phút và giây trong "Đang suy nghĩ câu trả lời"
    const updateTimeInterval = setInterval(() => {
        const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsedTime / 60);
        const seconds = elapsedTime % 60;
        const formattedTime = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        $typingIndicator.find('.time-count').text(formattedTime);
    }, 1000);

    let apiUrl = isSearchWebMode
        ? 'http://127.0.0.1:8000/api/chat/chatbot-with-search-web'
        : 'http://127.0.0.1:8000/api/chat/chatbot-with-gemini';
    $.ajax({
        url: apiUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ query: query }),
        success: function(data) {
            setTimeout(() => {
                clearInterval(updateTimeInterval);
                $typingIndicator.remove();
                processResponse(data);
                saveMessage(currentSessionId, 'bot', data.answer, data.lst_Relevant_Documents);
                $chatOutput.scrollTop($chatOutput.prop('scrollHeight'));
                isLoading = false;
                updateSendButtonState();
                $('#loading-indicator').text("");
            }, 800);
        }
    });
}

// Hàm xử lý dữ liệu để chatbot phản hồi và lấy ra trích dẫn
function processResponse(data) {
    const { answer, lst_Relevant_Documents } = data;
    let formattedAnswer = "";

    // Vì `answer` bây giờ là một chuỗi, chỉ cần thay thế ký tự xuống dòng bằng <br> để hiển thị đúng
    formattedAnswer = answer.replace(/\n/g, "<br>");
    formattedAnswer = formattedAnswer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Tạo một phần tử trống để từng từ sẽ được gõ vào đó
    const $chatOutput = $('#chat-output');
    const $botMessage = $(`
        <div class="chat-message bot">
            <div class="avatar bot-avatar" style="background-image: url('https://media.istockphoto.com/id/1333838449/vector/chatbot-icon-support-bot-cute-smiling-robot-with-headset-the-symbol-of-an-instant-response.jpg?s=612x612&w=0&k=20&c=sJ_uGp9wJ5SRsFYKPwb-dWQqkskfs7Fz5vCs2w5w950=');"></div>
            <div class="message"></div>
        </div>
    `);
    $chatOutput.append($botMessage);

    // Gọi typeMessage để hiển thị từng từ của câu trả lời
    typeMessage($botMessage.find(".message"), formattedAnswer, () => {
        // Kiểm tra nếu lst_Relevant_Documents tồn tại và không rỗng
        if (lst_Relevant_Documents && lst_Relevant_Documents.length > 0) {
            displayRelevantDocuments(lst_Relevant_Documents);
        }
    });
}

// Hàm cho chatbot in ra phản hồi cho user
function typeMessage($element, message, callback) {
    const words = message.split(" ");
    let index = 0;

    isTyping = true; // Bắt đầu trạng thái gõ
    updateSendButtonState(); // Vô hiệu hóa nút Send khi chatbot đang gõ

    const interval = setInterval(() => {
        if (index < words.length) {
            $element.append(words[index] + " ");
            index++;
            $element.parent().scrollTop($element.parent().prop('scrollHeight'));
        } else {
            clearInterval(interval);
            isTyping = false; // Kết thúc trạng thái gõ
            updateSendButtonState(); // Cập nhật trạng thái nút Send sau khi hoàn thành
            if (callback) callback(); // Gọi callback sau khi in xong
        }
    }, 25); // Điều chỉnh tốc độ gõ chữ (25ms mỗi từ)
}

// Hàm tạo thẻ cho lst_Relevant_Documents
function displayRelevantDocuments(documents) {
    const container = $('#relevant-documents-container');
    container.empty(); // Xóa các thẻ cũ nếu có

    // Tạo div chứa tiêu đề
    const title = $('<div class="references-title">Trích dẫn tham khảo</div>');
    container.append(title);

    // Tạo một div riêng cho các thẻ tài liệu
    const documentsWrapper = $('<div class="documents-wrapper"></div>');
    container.append(documentsWrapper);

    documents.forEach((doc, index) => {
        // Nếu là link (http/https) thì render ra link
        if (typeof doc === 'string' && doc.startsWith('http')) {
            const docElement = $(`
                <div class="relevant-document">
                    <a href="${doc}" target="_blank" rel="noopener noreferrer">${doc}</a>
                </div>
            `);
            documentsWrapper.append(docElement);
            return;
        }

        // Nếu là tài liệu có metadata thì giữ nguyên logic cũ
        const parts = doc.split('<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>');
        if (parts.length > 1) {
            const contentPart = parts[1].trim(); // Metadata phần đầu tiên
            const metadataPart = parts[0].trim();  // Nội dung tài liệu phần thứ hai

            // Trích xuất thông tin từ metadata, ví dụ: 'loai_van_ban' và 'so_hieu'
            const loaiVanBanMatch = metadataPart.match(/Loại văn bản: (.*)/);
            const soHieuMatch = metadataPart.match(/Số hiệu: (.*)/);

            // Lấy thông tin từ các nhóm đã trích xuất
            const loaiVanBan = loaiVanBanMatch ? loaiVanBanMatch[1] : "N/A";
            const soHieu = soHieuMatch ? soHieuMatch[1] : "N/A";

            // Giới hạn nội dung hiển thị (ví dụ: 20 ký tự đầu tiên)
            const shortContent = contentPart.length > 20 ? contentPart.substring(0, 20) + '...' : contentPart;

            // Tạo nội dung thẻ tài liệu mới
            const docElement = $(`
                <div class="relevant-document" data-full-content="${doc}">
                    ${loaiVanBan} ${soHieu}
                    <hr class="custom-hr">
                    ${shortContent}
                </div>
            `);

            // Thêm sự kiện click để mở rộng nội dung đầy đủ
            docElement.on('click', function() {
                const fullContent = $(this).data('full-content');
                openFullscreenDocument(fullContent);
            });

            documentsWrapper.append(docElement);
        }
    });
}

// Hàm mở nội dung đầy đủ khi click vào Trích dẫn
function openFullscreenDocument(content) {
    let formattedContent = content.replace(/\n/g, "<br>");
    // Thêm <br> trước số thứ tự, nhưng không thêm nếu trước đó là 'Điều: Điều' (có thể có khoảng trắng)
    formattedContent = formattedContent.replace(/((?<!Điều: Điều\s{0,10}))(\d+\.\s)/g, function(match, p1, p2) {
        if (p1 === "") return "<br>" + p2;
        return p1 + p2;
    });
    formattedContent = formattedContent.replace(/^<br>/, "");

    const overlay = $(`
        <div class="fullscreen-overlay">
            <div class="fullscreen-document">
                <div class="document-content">${formattedContent}</div>
            </div>
        </div>
    `);

    overlay.on('click', function(e) {
        if ($(e.target).is('.fullscreen-overlay')) {
            overlay.remove();
        }
    });

    $('body').append(overlay);
}

// Biến lưu session ID hiện tại
let currentSessionId = null;

// Hàm khởi tạo session mới
function startNewSession() {
    $.ajax({
        url: 'http://127.0.0.1:8000/api/session/start-session',
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
            currentSessionId = response.session_id; // Lưu session ID
            localStorage.setItem('session_id', currentSessionId); // Lưu vào localStorage
            console.log("New session started with ID:", currentSessionId);

            // Xóa khung chat và hiển thị tin nhắn mặc định
            $('#chat-output').empty();
            $('#relevant-documents-container').empty();
            const defaultMessage = `
                <div class="chat-message bot">
                    <div class="avatar bot-avatar" style="background-image: url('https://media.istockphoto.com/id/1333838449/vector/chatbot-icon-support-bot-cute-smiling-robot-with-headset-the-symbol-of-an-instant-response.jpg?s=612x612&w=0&k=20&c=sJ_uGp9wJ5SRsFYKPwb-dWQqkskfs7Fz5vCs2w5w950=');"></div>
                    <div class="message">Xin chào Bạn, Tôi là một trợ lý chuyên hỗ trợ về pháp luật Việt Nam. Bạn có câu hỏi gì xin đừng ngần ngại hỏi Tôi nhé!</div>
                </div>
            `;
            $('#chat-output').append(defaultMessage);
            // Reset về chế độ chat thường khi new chat
            isSearchWebMode = false;
            $('#toggle-search-web').removeClass('active').find('span').text('Chat');
            $('#user-query').attr('placeholder', 'Nhập tin nhắn ...');
            updateSearchWebButtonState(); // Enable Search Web button
        },
        error: function () {
            alert("Error: Unable to start new session.");
        }
    });
}

// Hàm xử lý khi user click New Chat
$('#new-chat').on('click', function (event) {
    event.preventDefault();
    if (confirm("Bạn có chắc chắn muốn bắt đầu một phiên trò chuyện mới?")) {
        localStorage.removeItem('session_id'); // Xóa session ID cũ
        startNewSession(); // Tạo session mới

        const $inputArea = $('#user-query');  // Sử dụng id 'user-query' thay vì class 'input-area'
        // Vô hiệu hóa input và thay đổi placeholder
        $inputArea.prop('disabled', false);  // Vô hiệu hóa input
        $inputArea.attr('placeholder', 'Nhập tin nhắn ...');  // Thay đổi placeholder

        loadChatSessions(); // Cập nhật lại danh sách phiên chat

        // Vô hiệu hóa Clear Chat khi bắt đầu một chat mới
        $clearChatButton.removeClass('active').addClass('disabled').prop('disabled', true);
    }
});

// Hàm lưu tin nhắn vào database
function saveMessage(sessionId, sender, message, references = null) {
    // Xử lý trường hợp references là chuỗi rỗng
    if (references === "") {
        references = [];
    }
    
    $.ajax({
        url: 'http://127.0.0.1:8000/api/session/save-message',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            session_id: sessionId,
            sender: sender,
            message: message,
            references: references
        }),
        success: function(response) {
            console.log("Message saved:", response);
        },
        error: function(xhr) {
            console.error("Error saving message:", xhr.responseText);
        }
    });
}

// Hàm load danh sách các phiên chat cũ
function loadChatSessions() {
    $.ajax({
        url: 'http://127.0.0.1:8000/api/session/get-sessions',
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            const sessions = response.sessions;
            const $chatSessions = $('#chat-sessions');
            $chatSessions.empty(); // Xóa nội dung cũ

            sessions.forEach(session => {
                const firstMessage = session.first_message || "No message yet";
                const truncatedMessage = firstMessage.length > 30 
                    ? firstMessage.substring(0, 30) + "..." 
                    : firstMessage;

                // Thêm icon ba chấm và menu Delete
                const sessionElement = $(
                    `<div class="chat-session" data-session-id="${session.id}">
                        <div class="chat-session-content">${truncatedMessage}</div>
                        <div class="session-menu-trigger">⋯</div>
                        <div class="session-menu">
                            <div class="session-menu-item delete-session">
                                <svg class="delete-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24"><path fill="#d00" d="M9 3a3 3 0 0 1 6 0h5a1 1 0 1 1 0 2h-1v15a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V5H4a1 1 0 1 1 0-2h5Zm8 2H7v15a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V5Zm-5 3a1 1 0 0 1 1 1v8a1 1 0 1 1-2 0V9a1 1 0 0 1 1-1Zm4 1a1 1 0 0 1 2 0v8a1 1 0 1 1-2 0V9Zm-8 0a1 1 0 0 1 2 0v8a1 1 0 1 1-2 0V9Z"/></svg>
                                Delete
                            </div>
                        </div>
                    </div>`
                );

                // Gắn sự kiện click để load lịch sử chat cho toàn bộ thẻ (trừ icon ba chấm và menu)
                sessionElement.on('click', function(e) {
                    // Nếu click vào menu hoặc icon ba chấm thì không load
                    if ($(e.target).hasClass('session-menu-trigger') || $(e.target).closest('.session-menu').length) return;
                    loadChatHistory(session.id);
                });

                // Hiện menu khi click vào ba chấm
                sessionElement.find('.session-menu-trigger').on('click', function(e) {
                    e.stopPropagation();
                    const $menu = $(this).siblings('.session-menu');
                    // Nếu menu đang hiện, ẩn nó đi. Nếu đang ẩn, ẩn tất cả menu khác và hiện menu này.
                    if ($menu.is(':visible')) {
                        $menu.hide();
                    } else {
                        $('.session-menu').hide();
                        $menu.show();
                    }
                });

                // Ẩn menu khi click ra ngoài
                $(document).on('click', function() {
                    $('.session-menu').hide();
                });

                // Xử lý xóa phiên chat
                sessionElement.find('.delete-session').on('click', function(e) {
                    e.stopPropagation();
                    if (confirm('Bạn có chắc chắn muốn xóa phiên chat này?')) {
                        const sessionId = session.id;
                        deleteChatSession(sessionId); // Gọi hàm xóa phiên chat
                        sessionElement.remove(); // Xóa khỏi giao diện
                    }
                });

                $chatSessions.append(sessionElement);
            });
        },
        error: function() {
            console.error("Error fetching chat sessions");
        }
    });
}

// Logic event khi load lại web thì sẽ load danh sách các phiên chat cũ
$(document).ready(function() {
    const $inputArea = $('#user-query');  // Sử dụng id 'user-query' thay vì class 'input-area'
    // Vô hiệu hóa input và thay đổi placeholder
    $inputArea.prop('disabled', true);  // Vô hiệu hóa input
    $inputArea.attr('placeholder', 'Click "Biểu tượng bút" để bắt đầu một phiên trò chuyện mới!');  // Thay đổi placeholder
});


// Hàm cập nhật trạng thái của nút Clear Chat
function updateClearChatButtonState() {
    // Kiểm tra nếu có tin nhắn từ người dùng trong chat-output
    const userMessagesExist = $chatOutput.find('.chat-message.user').length > 0;
    
    // Nếu có tin nhắn từ người dùng, bật nút Clear Chat
    if (userMessagesExist) {
        $clearChatButton.removeClass('disabled').addClass('active').prop('disabled', false);
    } else {
        $clearChatButton.removeClass('active').addClass('disabled').prop('disabled', true);
    }
}

// Lắng nghe sự kiện click vào một phiên chat từ sidebar
$('.chat-session').on('click', function() {
    // Khi người dùng click vào phiên chat, bật nút Clear Chat nếu có tin nhắn
    updateClearChatButtonState();
});

// Hàm load tài liệu tham khảo cho một tin nhắn
function loadMessageReferences(messageId) {
    // Xóa class selected từ tất cả tin nhắn bot
    $('.chat-message.bot').removeClass('selected');
    
    // Thêm class selected cho tin nhắn được click
    $(`.chat-message.bot[data-message-id="${messageId}"]`).addClass('selected');

    $.ajax({
        url: `http://127.0.0.1:8000/api/session/get-message-references/${messageId}`,
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            if (response.references && response.references.length > 0) {
                displayRelevantDocuments(response.references);
            } else {
                $('#relevant-documents-container').empty();
            }
        },
        error: function() {
            console.error("Error loading message references.");
        }
    });
}

// Hàm load lại lịch sử chat của một phiên
function loadChatHistory(sessionId) {
    console.log("Loading chat history for session ID:", sessionId);

    // Xóa phần trích dẫn tham khảo khi load lịch sử chat
    $('#relevant-documents-container').empty();

    // Xóa class selected từ tất cả các phiên chat và tin nhắn bot
    $('.chat-session').removeClass('selected');
    $('.chat-message.bot').removeClass('selected');
    
    // Thêm class selected cho phiên chat được chọn
    $(`.chat-session[data-session-id="${sessionId}"]`).addClass('selected');

    // Gọi API để lấy lịch sử chat
    $.ajax({
        url: `http://127.0.0.1:8000/api/session/get-chat-history/${sessionId}`,
        type: 'GET',
        contentType: 'application/json',
        success: function (response) {
            const chatHistory = response.chat_history;
            const $chatOutput = $('#chat-output');
            $chatOutput.empty();

            // Duyệt qua lịch sử chat và hiển thị từng tin nhắn
            chatHistory.forEach(chat => {
                const isBot = chat.sender === 'bot';
                
                let formattedMessage = chat.message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                formattedMessage = formattedMessage.replace(/\n/g, "<br>");

                const messageHtml = `
                    <div class="chat-message ${isBot ? 'bot' : 'user'}" data-message-id="${chat.id}">
                        <div class="avatar ${isBot ? 'bot-avatar' : 'user-avatar'}" 
                             style="background-image: url('${isBot ? 'https://media.istockphoto.com/id/1333838449/vector/chatbot-icon-support-bot-cute-smiling-robot-with-headset-the-symbol-of-an-instant-response.jpg?s=612x612&w=0&k=20&c=sJ_uGp9wJ5SRsFYKPwb-dWQqkskfs7Fz5vCs2w5w950=' : 'https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='}');">
                        </div>
                        <div class="message">${formattedMessage}</div>
                    </div>
                `;
                $chatOutput.append(messageHtml);
            });

            // Thêm sự kiện click cho tin nhắn của bot
            $('.chat-message.bot').on('click', function() {
                const messageId = $(this).data('message-id');
                loadMessageReferences(messageId);
            });

            const $inputArea = $('#user-query');
            $inputArea.prop('disabled', false);
            $inputArea.attr('placeholder', 'Nhập tin nhắn ...');

            updateClearChatButtonState();

            currentSessionId = sessionId;
            localStorage.setItem('session_id', sessionId);
            updateSearchWebButtonState(); // Enable Search Web button
        },
        error: function () {
            console.error("Error loading chat history.");
        }
    });
}

// Hàm add phiên chat hiện tại vào sidebar ngay sau khi user gửi tin nhắn
function addChatSessionToSidebar(sessionId, firstMessage) {
    const $chatSessions = $('#chat-sessions');
    const truncatedMessage = firstMessage.length > 30 
        ? firstMessage.substring(0, 30) + "..." 
        : firstMessage;

    const sessionElement = $(`
        <div class="chat-session" data-session-id="${sessionId}">
            <div class="chat-session-content">${truncatedMessage}</div>
        </div>
    `);

    // Gắn sự kiện click vào phiên chat mới
    sessionElement.on('click', function() {
        loadChatHistory(sessionId);
    });

    // Thêm phiên chat mới vào đầu danh sách
    $chatSessions.prepend(sessionElement);
}

// Lấy đối tượng của nút Clear Chat và chat-output
const $clearChatButton = $('#clear-chat');
const $chatOutput = $('#chat-output');

// Lắng nghe sự kiện click vào nút Clear Chat
$clearChatButton.on('click', function() {
    if (confirm("Bạn có chắc chắn muốn xóa phiên Chat này?")) {
        // Xóa chat ở frontend
        clearChatHistory();

        const $inputArea = $('#user-query');  // Sử dụng id 'user-query' thay vì class 'input-area'
        // Vô hiệu hóa input và thay đổi placeholder
        $inputArea.prop('disabled', true);  // Vô hiệu hóa input
        $inputArea.attr('placeholder', 'Click "Đoạn Chat Mới" để bắt đầu một phiên trò chuyện mới!');  // Thay đổi placeholder

        // Gửi yêu cầu đến backend để xóa chat
        deleteChatSession(currentSessionId);
    }
});

// Hàm xóa toàn bộ lịch sử chat trong giao diện
function clearChatHistory() {
    $chatOutput.empty();
    $('#relevant-documents-container').empty();
    updateClearChatButtonState(); // Cập nhật lại trạng thái của nút Clear Chat
}

// Hàm gửi yêu cầu xóa chat tới backend
function deleteChatSession(sessionId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/session/delete-session/${sessionId}`,
        type: 'DELETE',
        contentType: 'application/json',
        success: function(response) {
            console.log('Session deleted successfully');
            // Cập nhật lại danh sách các phiên chat trong sidebar
            loadChatSessions();
        },
        error: function() {
            console.error("Error deleting session.");
        }
    });
}