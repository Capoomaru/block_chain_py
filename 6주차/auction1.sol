pragma solidity ^0.6.0;

contract Auction1 {
    uint public maxValue;
    uint public endTime;
    uint public wishPrice;
    address payable owner;
    address payable bidder;
    bool public isEnd;

    constructor(uint _price, uint duration) public payable {
        owner = msg.sender;
        wishPrice = _price;
        endTime = now + duration;
        maxValue = 0;
        isEnd = false;
    }


    function bid() public payable {
        require(block.timestamp < endTime && isEnd == false, "Bid is end");
        require(msg.sender != owner, "Can't bid() Owner");
        require(msg.sender != bidder, "Can't bid() bidder");
        require(maxValue < msg.value, "price is smaller than prev max value");

        //이전 입찰자 환급
        bidder.transfer(maxValue);

        uint price = msg.value;
        //입찰가가 희망입찰가보다 높은 경우 환급
        if(msg.value >= wishPrice) {
            price = wishPrice;
            isEnd = true;

            msg.sender.transfer(msg.value - wishPrice);
        }
        //새로운 입찰자 정보 등록
        maxValue=price;
        bidder = msg.sender;
        emit bided(bidder, maxValue);
    }

    function finish() public payable {
        require(msg.sender == owner, "Can't finish without Owner");
        require(block.timestamp > endTime || isEnd , "You do not meet the conditions to close the auction");
        
        emit finalBid(bidder, maxValue);
        owner.transfer(maxValue);
        isEnd = true;
    }

    //새로운 입찰자 정보 log
    event bided(address, uint);
    //최종 입찰 정보 log
    event finalBid(address, uint);
}