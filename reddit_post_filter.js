const items = $input.all();
const processed = [];
const seenIds = new Set();

for (const item of items) {
  let data = item.json || {};
  
  const records = Array.isArray(data) ? data : [data];
  
  for (const post of records) {
    if (!post) continue;
    
    // Only skip comments, accept everything else
    if (post.dataType !== 'post') continue;
    
    const postId = post.id || post.postId || '';
    if (!postId || seenIds.has(postId)) continue;
    seenIds.add(postId);
    
    const title = post.title || '';
    const body = post.body || post.selftext || '';
    const content = title + (body ? '\n\n' + body : '');
    const upvotes = post.upVotes || post.ups || post.score || 0;
    const comments = post.numberOfComments || post.num_comments || post.commentsCount || post.numberOfreplies || 0;
    const category = post.category || post.communityName?.replace('r/', '') || 'tech';
    const isLinkPost = post.url && !post.url.includes('reddit.com') && !post.url.includes('redd.it');
    const redditThreadUrl = post.permalink
      ? (post.permalink.startsWith('http') ? post.permalink : 'https://reddit.com' + post.permalink)
      : `https://reddit.com/r/${category}`;

    processed.push({
      json: {
        post_id: postId,
        platform: 'Reddit',
        title: title,
        content: content.substring(0, 1500),
        body: body.substring(0, 800),
        url: redditThreadUrl,
        external_url: isLinkPost ? post.url : redditThreadUrl,
        is_news_link: isLinkPost || false,
        domain: post.domain || 'reddit.com',
        likes: upvotes,
        comments: comments,
        views: upvotes + comments,
        engagement_score: upvotes + (comments * 2),
        engagement_rate: ((upvotes / Math.max(upvotes + comments, 1)) * 100).toFixed(2),
        category: category,
        community_name: post.communityName || 'Reddit',
        author: post.username || post.author || 'anon',
        created_at: post.createdAt || post.created_utc || new Date().toISOString(),
        data_type: post.dataType
      }
    });
  }
}

console.log(`Total raw items: ${items.length} → Parsed posts: ${processed.length}`);
return processed.length > 0 ? processed : [{ json: { _skip: true, platform: 'Reddit', reason: 'No posts found' } }];
