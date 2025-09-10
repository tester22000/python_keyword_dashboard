$(document).ready(function() {
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    $('#date-input').val(new Date().toISOString().slice(0, 10))
    let currentPage = 1;
    let isLoading = false;
    let selectedIds = [];
    let isFiltering = false;

    function loadLinks(page) {
        if (isLoading) return;

        isLoading = true;
        
        const selectedDate = getSelectedDate()
        const selectedSite = $('#site-select').val();
        const searchTerm = $('#search-input').val();
        const searchKeyword =  $('#search-keyword').val();
        
        const params = {
            page: page,
            limit: 10,
            date: selectedDate
        };

        if (selectedSite) {
            params.name = selectedSite;
        }
        if (searchTerm) {
            params.search = searchTerm;
        }
        if (searchKeyword) {
            params.keyword = searchKeyword;
        }

        $.get('/api/links', params)
            .done(function(data) {
                if (data.links.length > 0) {
                    renderLinks(data.links);
                    if (data.has_more) {
                        currentPage++;
                    } else {
                        $(window).off('scroll'); 
                    }
                } else if (page === 1) {
                    $('#link-list').html('<p class="text-center text-gray-500 mt-4">검색 결과가 없습니다.</p>');
                }
            })
            .always(function() {
                isLoading = false;
            });
    }

    function renderLinks(links) {
        const linkList = $('#link-list');
        links.forEach(function(link) {
            const linkHtml = `
                <div class="bg-white p-4 my-2 rounded-md shadow flex items-start">
                    <input type="checkbox" data-id="${link.id}" class="form-checkbox h-5 w-5 text-blue-600 rounded mt-1">
                    <div class="ml-4 flex-1">
                        <span class="text-gray-500 text-sm font-semibold">${link.name}</span>
                        <a href="${link.link}" target="_blank" class="block text-blue-600 font-bold hover:underline">${link.title}</a>
                    </div>
                </div>
            `;
            linkList.append(linkHtml);
        });
    }

    function renderKeywords(keywords) {
        const keywordList = $('#keyword-list');
        keywordList.empty(); 
        if (keywords.length > 0) {
            keywords.forEach(function(keyword) {
                const keywordHtml = `
                    <li class="p-2 hover:bg-gray-100 rounded-md cursor-pointer keyword-item" data-keyword="${keyword.keyword}">
                        <span class="text-gray-700">${keyword.keyword}</span>
                        <span class="text-xs text-gray-500 ml-2">(${keyword.point})</span>
                    </li>
                `;
                keywordList.append(keywordHtml);
            });
        } else {
            keywordList.html('<li class="text-gray-500 p-2">결과 없음</li>');
        }
    }

    function getSelectedDate() {
        const inputDate = $('#date-input').val()
        if(inputDate){
            return inputDate.replace(/-/g,'')
        }
        return today
    }
    function loadSites() {
        const selectedDate = getSelectedDate()
        $.get('/api/site_names', { date: selectedDate })
            .done(function(data) {
                const select = $('#site-select');
                select.empty().append('<option value="">사이트를 선택하세요</option>');
                data.site_names.forEach(function(name) {
                    select.append(`<option value="${name}">${name}</option>`);
                });
            });
    }

    function loadKeywords() {
        const selectedDate = getSelectedDate()
        const selectedSite = $('#site-select').val();
        const keywordSearchTerm = $('#keyword-search-input').val();

        const params = { date: selectedDate };
        if (selectedSite) {
            params.name = selectedSite;
        }
        if (keywordSearchTerm) {
            params.keyword = keywordSearchTerm;
        }

        $.get('/api/keywords', params)
            .done(function(data) {
                renderKeywords(data.keywords);
            });
    }
    
    function reQuery() {
        currentPage = 1;
        $('#link-list').empty();
        $(window).on('scroll', handleScroll); 
        loadLinks(currentPage);
    }
    
    function updateDeleteButton() {
        if (selectedIds.length > 0) {
            $('#delete-button-container').removeClass('hidden');
        } else {
            $('#delete-button-container').addClass('hidden');
        }
    }

    const handleScroll = function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            loadLinks(currentPage);
        }
    };
    $(window).on('scroll', handleScroll);

    $('#date-input').on('change', function() {
        $("#search-input").val("");
        $('#keyword-search-input').val('')
        $('#search-keyword').val('')
        reQuery();
        loadSites(); 
        loadKeywords();
    });

    $('#site-select').on('change', function() {
        $("#search-input").val("");
        $('#keyword-search-input').val('');
        $('#search-keyword').val('')
        reQuery();
        loadKeywords();
    });

    let searchTimeout;
    $('#search-input').on('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() {
            reQuery();
        }, 500); 
    });
    
    let keywordSearchTimeout;
    $('#keyword-search-input').on('input', function() {
        clearTimeout(keywordSearchTimeout);
        keywordSearchTimeout = setTimeout(function() {
            loadKeywords();
        }, 500); 
    });

    $('#link-list').on('change', 'input[type="checkbox"]', function() {
        const id = $(this).data('id');
        if ($(this).is(':checked')) {
            if (!selectedIds.includes(id)) {
                selectedIds.push(id);
            }
        } else {
            selectedIds = selectedIds.filter(item => item !== id);
        }
        updateDeleteButton();
    });
    
    $('#keyword-list').on('click', '.keyword-item', function() {
        const keyword = $(this).data('keyword');
        if(keyword === $("#search-keyword").val()){
            $(this).css('font-weight','normal')
            $('#search-keyword').val('')
        }else{
            $('#keyword-list>li').css('font-weight','normal')
            $(this).css('font-weight','bold')
            const keyword = $(this).data('keyword');
            $('#search-keyword').val(keyword)
        }
        reQuery();
    });

    $('#delete-button').on('click', function() {
        if (confirm(`${selectedIds.length}개의 항목을 정말 삭제하시겠습니까?`)) {
            $.ajax({
                url: '/api/links',
                type: 'DELETE',
                contentType: 'application/json',
                data: JSON.stringify({ ids: selectedIds }),
                success: function(response) {
                    alert(response.message);
                    selectedIds = [];
                    updateDeleteButton();
                    reQuery(); 
                },
                error: function(xhr, status, error) {
                    alert('삭제 중 오류가 발생했습니다.');
                    console.error('삭제 오류:', error);
                }
            });
        }
    });

    loadSites();
    loadKeywords();
    reQuery();
});